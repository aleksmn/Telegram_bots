# Алексей
import telebot
from config import api_token
import logging
import json
import random

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это бот для изучения английского языка")


    

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Начинаем работу бота...")

    bot.polling(non_stop=True, logger_level=logging.INFO)
    