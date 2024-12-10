import telebot
import json
import logging
from datetime import date, timedelta

from config import api_token


TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Бот для записи на процедуры запущен.")



def add_appointment(date, time, client):
    # Чтение существующих данных из файла
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": []}

    # Добавление новой записи
    new_appointment = {...}
    data['appointments'].append(...)


    # Запись обновленных данных в файл
    ...



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Начинаем работу бота...")
    
    bot.polling(none_stop=True)