import telebot
import json
import logging

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
    new_appointment = {'date': date, 'time': time, 'client': client}
    data['appointments'].append(new_appointment)

    # Запись обновленных данных в файл
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Начинаем работу бота...")
    
    bot.polling(none_stop=True)