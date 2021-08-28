from telebot import TeleBot
from telebot import types
import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def id_driver():
    global connection
    query = 'SELECT id_telegram FROM users WHERE driver=True;'
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchone()[0]


with open('token.txt') as f:
    token = f.readline().rstrip()

with open('db.txt') as f:
    ip = f.readline().rstrip()
    port = f.readline().rstrip()
    user = f.readline().rstrip()
    password = f.readline().rstrip()

connection = create_connection("sm_app", user, password, ip, port)
chat_id_Nikita = id_driver()
rating = {'common': []}
feedback = ""
bot = TeleBot(token)