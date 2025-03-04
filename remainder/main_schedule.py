import telebot
import logging
import time
import threading
import schedule

from config import api_token


API_TOKEN = api_token
bot = telebot.TeleBot(API_TOKEN)



def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=["remind"])   
def set_reminder(message):
    # Пример команды
    # /remind 3600 напоминание
    chat_id = message.chat.id
    parts = message.text.split(' ', 2)
    delay = int(parts[1])  # Время в секундах
    reminder_message = parts[2]  # Сообщение напоминания

    def regular_remainder():
        bot.send_message(chat_id, reminder_message)

    schedule.every(1).seconds.do(regular_remainder)



if __name__ == "__main__":

    threading.Thread(target=schedule_thread).start()

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Начинаем работу бота...")


    bot.polling(non_stop=True)

