from function.bot import *

st = False

# Провера на наличие пользователя в БД
def chech_user_in_db(id):
    global connection
    query = 'SELECT id_telegram FROM users;'
    cursor = connection.cursor()
    cursor.execute(query)
    row = [i[0] for i in cursor]
    if id not in row:
        query = 'INSERT INTO users(id_telegram) VALUES (' + str(id) + ');'
        cursor.execute(query)
        connection.commit()
    cursor.close()

# Вывод общего и конкретного рейтингов
def view_rating(id):
    global connection
    rating = []
    cursor = connection.cursor()
    cursor.execute('SELECT count(rate), sum(rate) FROM rating;')
    rating.append(cursor.fetchall()[0])
    cursor.execute('SELECT count(rate), sum(rate) FROM rating WHERE id =' + str(id) + ';')
    rating.append(cursor.fetchall()[0])
    cursor.close()
    return rating

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
    global st
    if not st:
        chech_user_in_db(message.from_user.id)
        st = True
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True)
    key_1 = types.KeyboardButton('Оценить поездку')
    key_2 = types.KeyboardButton('Вывести рейтинг')
    key_3 = types.KeyboardButton('Отменить оценку')
    key_4 = types.KeyboardButton('Отправить чаевые/отзыв')
    keyboard.add(key_1, key_2, key_3, key_4)
    msg = bot.send_message(message.from_user.id, text='Выберите команду', reply_markup=keyboard)
