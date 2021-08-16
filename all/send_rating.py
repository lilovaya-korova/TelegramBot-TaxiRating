from all.common import *


@bot.message_handler(regexp="Вывести*")
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