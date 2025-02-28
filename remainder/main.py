import telebot
import logging
import time
import threading

from config import api_token

API_TOKEN = api_token
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения напоминаний
reminders = {}

def reminder_thread(chat_id, message, delay):
    time.sleep(delay)
    bot.send_message(chat_id, message)
    del reminders[chat_id]  # Удаляем напоминание после отправки

@bot.message_handler(commands=['remind'])
def set_reminder(message):
    try:
        # Пример команды: /remind 10 Напоминание
        parts = message.text.split(' ', 2)
        delay = int(parts[1])  # Время в секундах
        reminder_message = parts[2]  # Сообщение напоминания

        chat_id = message.chat.id
        if chat_id in reminders:
            bot.send_message(chat_id, "У вас уже есть активное напоминание.")
            return

        # Запускаем поток для напоминания
        threading.Thread(target=reminder_thread, args=(chat_id, reminder_message, delay)).start()
        reminders[chat_id] = reminder_message
        bot.send_message(chat_id, f"Напоминание установлено на {delay} секунд.")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Используйте: /remind <время в секундах> <сообщение>")

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    logging.info("Начинаем работу бота...")

    bot.polling(non_stop=True)