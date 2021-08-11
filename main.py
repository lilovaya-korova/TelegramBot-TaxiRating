import telebot
from telebot import types

with open('token.txt') as f:
    token = f.readline().rstrip()
    chat_id_Nikita = f.readline().rstrip()

bot = telebot.TeleBot(token)
rating = {'common': []}
feedback = ""

# -------------------------------- Общие запросы
# Функция для уточнения действий пользователя
def correcting_answer(message, text, func):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key_1 = types.KeyboardButton('Да')
    key_2 = types.KeyboardButton('Нет')
    keyboard.add(key_1, key_2)
    bot.reply_to(message, 'Вы действительно хотите ' + text + '?', reply_markup=keyboard)
    bot.register_next_step_handler(message, func)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == 'Оценить поездку':
        rate_trip(message)
    elif message.text == 'Вывести рейтинг':
        send_rating(message)
    elif message.text == 'Отменить оценку':
        cancel_grade(message)
    elif message.text == 'Отправить чаевые/отзыв':
        post_message(message)
    else:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
        key_1 = types.KeyboardButton('Оценить поездку')
        key_2 = types.KeyboardButton('Вывести рейтинг')
        key_3 = types.KeyboardButton('Отменить оценку')
        key_4 = types.KeyboardButton('Отправить чаевые/отзыв')
        keyboard.add(key_1, key_2, key_3, key_4)
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
    elif call.text == 'Отправить чаевые/отзыв':
        post_message(call)
    else:
        start(call)


# --------------------------------  Оценка поездки
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


# -------------------------------- Рейтинг
# подсчет рейтинга
@bot.callback_query_handler(func=lambda call: True)
def calculation_rating(call):
    global rating
    rating['common'].append(int(call.text))
    if call.from_user.id in rating:
        rating[call.from_user.id].append(int(call.text))
    else:
        rating.update({call.from_user.id: [int(call.text)]})
    start(call)


# вывод рейтинга
@bot.message_handler(commands=['rating'])
def send_rating(message):
    global rating
    if rating["common"]:
        reply = "Общий рейтинг равен " + str(round(sum(rating['common']) / len(rating['common']), 2))
        if message.from_user.id in rating:
            reply += '\nВаш рейтинг равен ' + str(
                round(sum(rating[message.from_user.id]) / len(rating[message.from_user.id]), 2))
        else:
            reply += "\nВаш рейтинг отсутствует"
    else:
        reply = "Рейтинг отсутствует"
    bot.reply_to(message, reply)


# -------------------------------- Отмена оценки
@bot.message_handler(commands=['cancel'])
def cancel_grade(message):
    global rating
    if message.from_user.id in rating:
        correcting_answer(message, 'отменить оценку', cancel_grade_func)
    else:
        bot.reply_to(message, 'У вас нет оценки')


@bot.callback_query_handler(func=lambda call: True)
def cancel_grade_func(call):
    global rating
    if call.from_user.id in rating and call.text == "Да":
        if rating[call.from_user.id] != []:
            rating["common"].remove(rating[call.from_user.id].pop())
        else:
            bot.reply_to(call, 'У вас нет оценки')
    start(call)


# -------------------------------- Чаевые и отзыв
# Выбор между чаевыми и отзывом
@bot.message_handler(commands=['message'])
def post_message(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key_1 = types.KeyboardButton('Отзыв')
    key_2 = types.KeyboardButton('Чаевые')
    keyboard.add(key_1, key_2)
    bot.reply_to(message, 'Что вы хотите отправить Никите?', reply_markup=keyboard)
    bot.register_next_step_handler(message, post_message_func)


# Разделение ветки
@bot.callback_query_handler(func=lambda call: True)
def post_message_func(message):
    if message.text == 'Чаевые':
        text = '💸'
        bot.send_message(chat_id_Nikita, text)
        bot.reply_to(message, '*Чаевые отправлены Никите*', parse_mode='Markdown')
        start(message)
    else:
        bot.send_message(message.from_user.id, 'Напишите анонимный отзыв Никите')
        bot.register_next_step_handler(message, send_feedback)


# Убеждаемся, что отзыв нормальный
@bot.callback_query_handler(func=lambda call: True)
def send_feedback(message):
    global feedback
    feedback = message.text
    correcting_answer(message, 'отправить этот отзыв', send_feedback_func)


@bot.callback_query_handler(func=lambda call: True)
def send_feedback_func(message):
    if message.text == "Да":
        bot.send_message(chat_id_Nikita, feedback)
        bot.reply_to(message, '*Отзыв отправлен Никите*', parse_mode='Markdown')
    else:
        bot.reply_to(message, '*Отзыв не отправлен Никите*', parse_mode='Markdown')
    start(message)


bot.polling()
