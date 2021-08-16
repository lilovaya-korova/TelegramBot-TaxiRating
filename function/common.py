from function.bot import *


# Функция для уточнения действий пользователя
def correcting_answer(message, text, func):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    key_1 = types.KeyboardButton('Да')
    key_2 = types.KeyboardButton('Нет')
    keyboard.add(key_1, key_2)
    bot.reply_to(message, 'Вы действительно хотите ' + text + '?', reply_markup=keyboard)
    bot.register_next_step_handler(message, func)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
    key_1 = types.KeyboardButton('Оценить поездку')
    key_2 = types.KeyboardButton('Вывести рейтинг')
    key_3 = types.KeyboardButton('Отменить оценку')
    key_4 = types.KeyboardButton('Отправить чаевые/отзыв')
    keyboard.add(key_1, key_2, key_3, key_4)
    msg = bot.send_message(message.from_user.id, text='Выберите команду', reply_markup=keyboard)
