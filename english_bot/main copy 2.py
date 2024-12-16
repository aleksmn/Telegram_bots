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




@bot.message_handler(commands=["addword"])  # /addword apple яблоко
def handle_addword(message):

    words = message.text.split()[1:]
    
    word, translation = words[0].lower(), words[1].lower()










# Всегда последнее
@bot.message_handler(func=lambda message: True)
def handle_questions(message):
    text = message.text.lower()
    if text == "как тебя зовут?":
        bot.send_message(message.chat.id, "У меня пока нет имени")
    elif text == "расскажи о себе":
        bot.send_message(message.chat.id, "Я бот для изучения английского языка")
    elif text == "расскажи шутку":
        bot.send_message(message.chat.id, "У меня плохое чувство юмора. Советую спросить об этом в интернете")
    elif text == "как дела?":
        bot.send_message(message.chat.id, "Хорошо. Я рад, что буду полезным ботом")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Начинаем работу бота...")
    logging.warning("ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ")
    logging.error("ОШИБКИ")

    bot.polling(non_stop=True)
    