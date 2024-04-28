# умозаключатель

бот доступен по ссылке [@zhukov_gpt_bot](https://t.me/zhukov_gpt_bot)

недавно открыли доступ к самой интересной части сервиса Yandex Foundation Models — нейросети YaGPT2. на данный момент это самая прогрессивная генеративная модель на русском языке, которую предлагают использовать для бизнес-целей: для анализа текстовой информации, для создания контента и для чат-ботов, чтобы, например, заменить упростить работу операторов и техподдержки.

меня же заинтересовал другой аспект работы с нейросетью, а именно температура ответа на запрос.

нейросеть может выполнять задачи, требующие как творческого подхода, так и консервативности. например, предлагая нейросети сделать тезисную выжимку из научной работы, мы не ждём что она будет что-то выдумывать. а генерируя описания для карточек своих товаров на озоне мы можем дать небольшую волю для творчества и более яркого описания аромасвечей. на это как раз и влияет параметр температуры.

причем же тут температура? хорошим объяснением была бы аналогия с температурой человека, когда он начинает бредить после 39, как и нейросеть со своими ответами. на деле же это некая отсылка к распределению Больцмана из термодинамики. распределение описывает вероятность состояний системы. 

проводя аналогию с нейросетью, существуют такие состояния, где система уверена в ответе, например 2+2=4, потому что математика, или где системе дают волю и получается 2+2=5, потому что единицу наколдовал волшебник. всё это — разная вероятность, где высказывания зачастую объяснены и связаны логически, но с использованием очень странных предикатов. 

"устами младенца глаголет истина", "сумасшедший значит гений", и прочие крылатые выражения отсылают нас именно к прогрессивности, гениальности и порой даже истинности сломанных/несформированных систем (в данном случае систем мышления  у людей). продолжая аналогию, стоит отметить, что зачастую подобная гениальность (в музыке, науке и прочих областях) обусловлена первично развитием системы, и только затем отступлением от норм. только более сформированная, масштабная система может воспринять "ошибку" в системе сумасшедшего или ребенка, использовав её как ключ к совершенствованию и созданию нового. для двух сломанных систем большинство параметров не найдут применения, и тем более понимания. кстати, вероятно, параметр высокой температуры применим и к вышеназванным системам мышления.


использовав api языковой модели, телеграм и пару часов времени я создал бота "умозаключатель". он выдает случайное и очень необычное умозаключение. думаю, это пригодится людям, чья деятельность связана с творчеством. в периоды кризиса он может подкинуть очень интересную мысль для сценария книги/дизайна интерьера/лора игры/etc, выдав вам системную ошибку. распорядитесь ей по своему усмотрению. 
