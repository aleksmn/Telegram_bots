import telebot
from config import api_token
import logging
import json

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это бот для изучения английского языка")



@bot.message_handler(commands=['learn'])
def handle_learn(message):
    bot.send_message(message.chat.id, "Обучение сейчас начнется!")


@bot.message_handler(commands=['addword']) # /addword apple яблоко
def handle_addword(message):
    global user_data
    logging.info(f"Сообщение {message.text}")
    # bot.send_message(message.chat.id, "Добавляем новое слово")
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id, {})

    words = message.text.split()[1:]
    if len(words) == 2:
        word, translation = words[0].lower(), words[1].lower()
        user_dict[word] = translation

        user_data[chat_id] = user_dict

        with open("user_data.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        bot.send_message(chat_id, "Слово добавлено")
    else:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова. Пример команды: /addword apple яблоко")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "У меня пока нет имени")
    elif message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "Я бот для изучения английского языка")



"""
learn - Обучение
addword - Добавить слово

"""        

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Начинаем работу бота...")

    bot.polling(non_stop=True, logger_level=logging.INFO)
    