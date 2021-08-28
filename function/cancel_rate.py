from function.common import *


# Удаление оценки из БД
def cancel_rate(id):
    global connection
    query = 'DELETE FROM rating WHERE id=' + str(id) + 'AND number = (SELECT MAX(number) FROM rating);'
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()


@bot.message_handler(regexp="Отменить оценку")
def cancel_grade(message):
    rating = view_rating(message.from_user.id)
    if rating[1][1]:
        correcting_answer(message, 'отменить оценку', cancel_grade_func)
    else:
        bot.reply_to(message, "У вас нет оценки")
        start(message)


@bot.callback_query_handler(func=lambda call: True)
def cancel_grade_func(message):
    if message.text == "Да":
        cancel_rate(message.from_user.id)
        bot.reply_to(message, "Оценка отменена")
    start(message)
