# TelegramBot-TaxiRating
Цель телеграмм-бота - выставление оценок поездки на "такси" вашего друга.

# Доступные функции:
- Отправить оценку (от 1 до 10)
- Отменить оценку
- Посмотреть рейтинг
- Отправить чаевые или отзыв
 
# Дополнительные настройки:
В корне программы должны лежать файлы token.txt и db.txt

Файл *token.txt* содержит:
- токен бота

Файл *db.txt* построчно содержит следующие данные:
- ip-адрес sql-сервера
- порт, на котором работает sql-сервер
- имя пользователя, который работает с sql-сервером
- пароль к sql-серверу 

**Файл app содержит backup postgresql**

# To-do
- Модерация поездки
- Ограничение по времени (чтобы не спамить оценками)
