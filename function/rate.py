from function.common import *


# добавление оценки в БД
def add_rate(id, rate):
    global connection
    query = 'INSERT INTO rating VALUES (' + str(id) + ',' + str(rate) + ');'
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


# оценить поездку
@bot.message_handler(regexp="Оценить поездку")
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
    add_rate(call.from_user.id, call.text)
    rating['common'].append(int(call.text))
    if call.from_user.id in rating:
        rating[call.from_user.id].append(int(call.text))
    else:
        rating.update({call.from_user.id: [int(call.text)]})
    start(call)
