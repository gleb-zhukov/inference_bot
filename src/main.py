import os
import json
import ydb
import ydb.iam
import telebot
from telebot.types import KeyboardButton
from telebot import types
import time
import requests
import json

permit = 1 #1 - доступ разрешен, 0 - доступ запрещен

ydb_endpoint=os.getenv('YDB_ENDPOINT')
ydb_database=os.getenv('YDB_DATABASE')

tg_token = os.getenv('TG_TOKEN')

gpt_token = ''

# Create driver in global space.
driver = ydb.Driver(
  endpoint=ydb_endpoint,
  database=ydb_database,
  credentials=ydb.iam.MetadataUrlCredentials() #use in YC
)
# Wait for the driver to become active for requests.
driver.wait(fail_fast=True, timeout=5)
session = driver.table_client.session().create()

bot = telebot.TeleBot(tg_token)

start_msg = 'нейросетевое умозаключение.\n' \
        'максимальная температура.\n\n' \
        'присоединяйся: @zhukov_tech'

about_msg = 'нейросетевое умозаключение.\n\n' \
        'используются технологии синтеза текста с максимальной температурой ответа на запрос. '\
        'телом запроса (промта) является просьба предоставить необычное высказывание, сконфигурированное '\
        'вариативно в каждом запросе.\n\nтемпературой в нейросетевом синтезе принято считать '\
        'некое "лавирование" нейросети между консервативностью и разнообразием ответа.\n\n'\
        'подробнее о работе бота можно прочитать здесь, присоединяйся: @zhukov_tech'

error_msg = 'ведутся технические работы\n\nразработчик/по всем вопросам: @konstela\nподписывайся: @zhukov_tech'



def gen_text():
    prompt = {
        "modelUri": "gpt://b1gah8egappp6q13pon0/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 1,
            "maxTokens": "100"
        },
        "messages": [
            {
                "role": "user",
                "text": "сгенерируй самое необычное умозаключение"
            }
        ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
    "Authorization": 'Bearer ' + gpt_token
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    print(result)

    json_result = json.loads(result)
    text = json_result['result']['alternatives'][0]['message']['text']
    return text


def keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton("gen"),KeyboardButton("о боте"))
    return markup

def ydb_get_user_spot(user_id):
  result_sets = session.transaction().execute(f'select spot from user where id == {user_id}', commit_tx=True,)
  if not result_sets[0].rows: #если ответ пустой, значит пользователя в базе нет
    return 0
  else:
    for row in result_sets[0].rows:
        spot = row.spot
        return spot


def ydb_update_user(user_id, spot):
  session.transaction().execute(
    f'upsert into user (id, spot) values ({user_id}, {spot})',
    commit_tx=True,
    )

def ydb_update_text(text):
    id = 0
    result_sets = session.transaction().execute(f'SELECT id FROM text ORDER BY id DESC LIMIT 1', commit_tx=True,)
    for row in result_sets[0].rows:
        id = row.id
    id = id + 1
    session.transaction().execute(
    f'upsert into text (id, text) values ({id}, "{text}")',
    commit_tx=True,
    )

def ydb_get_text(spot):
    result_sets = session.transaction().execute(f'select text from text where id == {spot}', commit_tx=True,)
    if not result_sets[0].rows:
        print('error, no data in ydb, func ydb_get_text')
    else: # иначе если ответ есть, отдаем 
        for row in result_sets[0].rows:
            text = row.text
            return text



@bot.message_handler(commands=["start"]) #если юзер запускает бота
def start_message(message):
    user_id = message.from_user.id
    if permit == 0:
        if user_id != 321588402: #мне можно
            bot.send_message(user_id, error_msg)
    else:
        bot.send_message(user_id, start_msg, reply_markup=keyboard())
        if ydb_get_user_spot(user_id) == 0:
            spot = 1
            ydb_update_user(user_id, spot)


@bot.message_handler(func=lambda message:True)
def all_messages(message):
    user_id = message.from_user.id
    if permit == 0:
        if user_id != xxx: #мне можно
            bot.send_message(user_id, error_msg)
            return
    if message.text == "gen":
        spot = ydb_get_user_spot(user_id)
        spot = spot + 1
        text = ydb_get_text(spot)
        time.sleep(1)
        bot.send_message(user_id, text)
        ydb_update_user(user_id, spot)
        return
    if message.text == "о боте":
        bot.send_message(user_id, about_msg)
        return
    if message.text == 'real gen':
        if user_id == 321588402: #мне можно
            text = gen_text()
            bot.send_message(user_id, text)
            return
    else:
        if user_id == 321588402:
            text = message.text
            ydb_update_text(text)



def handler(event,context):
    global gpt_token
    gpt_token = context.token["access_token"]
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])
    return {
    'statusCode': 200,
    'body': 'ok',
    }
