from all.common import *


#выбор между чаевыми и отзывом
@bot.message_handler(regexp="Отправить*")
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
