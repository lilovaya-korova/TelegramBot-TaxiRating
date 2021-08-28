from function.common import *


@bot.message_handler(regexp="Вывести*")
def send_rating(message):
    rating = view_rating(message.from_user.id)
    if rating[0][1]:
        reply = "Общий рейтинг равен " + str(round(rating[0][1] / rating[0][0], 2))
        if rating[1][1]:
            reply += '\nВаш рейтинг равен ' + str(round(rating[1][1] / rating[1][0], 2))
        else:
            reply += "\nВаш рейтинг отсутствует"
    else:
        reply = "Рейтинг отсутствует"
    bot.reply_to(message, reply)
