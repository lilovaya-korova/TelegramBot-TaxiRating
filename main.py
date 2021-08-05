import telebot
from telebot import types

with open('token.txt') as f:
    token = f.read()

bot = telebot.TeleBot(token)
rating = {'common': [0, 0]}


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == 'Оценить поездку':
        rate_trip(message)
    elif message.text == 'Вывести рейтинг':
        send_rating(message)
    elif message.text == 'Отменить оценку':
        cancel_grade(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
        key_1 = types.KeyboardButton('Оценить поездку')
        key_2 = types.KeyboardButton('Вывести рейтинг')
        key_3 = types.KeyboardButton('Отменить оценку')
        keyboard.add(key_1, key_2, key_3)
        msg = bot.send_message(message.from_user.id, text='Выберите команду', reply_markup=keyboard)
        bot.register_next_step_handler(msg, command)


@bot.callback_query_handler(func=lambda call: True)
def command(call):
    if call.text == 'Оценить поездку':
        rate_trip(call)
    elif call.text == 'Вывести рейтинг':
        send_rating(call)
    elif call.text == 'Отменить оценку':
        cancel_grade(call)
    else:
        start(call)



# функция для оценки поездки
@bot.message_handler(commands=['start'])
def rate_trip(message):
    question = 'Оцените поездку Никиты'
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    key_1 = types.KeyboardButton('1')
    key_2 = types.KeyboardButton('2')
    key_3 = types.KeyboardButton('3')
    key_4 = types.KeyboardButton('4')
    key_5 = types.KeyboardButton('5')
    key_6 = types.KeyboardButton('6')
    key_7 = types.KeyboardButton('7')
    key_8 = types.KeyboardButton('8')
    key_9 = types.KeyboardButton('9')
    key_10 = types.KeyboardButton('10')
    keyboard.add(key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10)
    msg = bot.reply_to(message, question, reply_markup=keyboard)
    bot.register_next_step_handler(msg, calculation_rating)


# подсчет рейтинга
@bot.callback_query_handler(func=lambda call: True)
def calculation_rating(call):
    global rating
    try:
        rating['common'][0] = rating['common'][0] + int(call.text)
        rating['common'][1] += 1
        try:
            rating[call.from_user.id][0] = rating[call.from_user.id][0] + int(call.text)
            rating[call.from_user.id][1] += 1
        except:
            rating.update({call.from_user.id: [int(call.text), 1]})
    except:
        pass
    start(call)


# вывод рейтинга
@bot.message_handler(commands=['rating'])
def send_rating(message):
    global rating
    try:
        reply = "Общий рейтинг равен " + str(rating['common'][0] / rating['common'][1]) + '\nВаш рейтинг равен ' + str(
            rating[message.from_user.id][0] / rating[message.from_user.id][1])
    except:
        reply = "Рейтинг отсутствует"
    bot.reply_to(message, reply)


@bot.message_handler(commands=['cancel'])
def cancel_grade(message):
    global rating
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key_1 = types.KeyboardButton('Да')
    key_2 = types.KeyboardButton('Нет')
    keyboard.add(key_1, key_2)
    bot.reply_to(message, 'Вы действительно хотите отменить последнюю оценку?', reply_markup=keyboard)
    bot.register_next_step_handler(message, cancel_grade_func)
    '''try:
        reply = "Общий рейтинг равен " + str(rating['common'][0] / rating['common'][1]) + '\nВаш рейтинг равен ' + str(
            rating[message.from_user.id][0] / rating[message.from_user.id][1])
    except:
        reply = "Рейтинг отсутствует"
    bot.reply_to(message, reply)'''


@bot.callback_query_handler(func=lambda call: True)
def cancel_grade_func(call):
    global rating
    if call.from_user.id in rating and call.text == "Нет":
        print(rating)
    elif call.text == "Да":
        bot.reply_to(call, 'У вас нет оценки')
    start(call)


bot.polling()
