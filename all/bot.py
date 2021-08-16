from telebot import TeleBot
from telebot import types


with open('token.txt') as f:
    token = f.readline().rstrip()
    chat_id_Nikita = f.readline().rstrip()


rating = {'common': []}
feedback = ""
bot = TeleBot(token)