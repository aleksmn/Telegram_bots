import telebot
import logging
from config import api_token

# pip install pyTelegramBotAPI

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.info("Обработчик команды start")
    logging.info(message.chat.id)

    bot.send_message(message.chat.id, "Привет! Это твой бот!")



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    logging.info("Начинаем работу бота...")

    bot.polling(non_stop=True)