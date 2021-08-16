from all.common import *


@bot.message_handler(regexp="Отменить оценку")
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