import telebot
from config import api_token
import logging
import json
import random
import time

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)

try:
    with open("user_data.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}


@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это бот для изучения английского языка")



@bot.message_handler(commands=['learn'])
def handle_learn(message):
    logging.debug(f"handle_learn")

    user_words = user_data.get(str(message.chat.id), {})

    # Проверяем, есть ли у пользователя слова
    if not user_words:
        bot.send_message(message.chat.id, "Твой словарь пуст!")
        return
    


    try:
        # тернарный оператор
        words_number = int(message.text.split()[1]) if len(message.text.split()) > 1 else 1
        
        ask_translation(message.chat.id, user_words, words_number)
    except ValueError:
        bot.send_message(message.chat.id, "Используй команду /learn <количество> для изучения слов.")



def ask_translation(chat_id, user_words, words_number):

    if words_number > 0:

        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова '{word}'.")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_number)

    else:
        bot.send_message(chat_id, "Урок закончен")


def check_translation(message, translation, words_number):
    logging.debug("check_translation")
    logging.debug(f"{message}, {translation}")
    user_translation = message.text.strip().lower()
    # сравниваем перевод пользователя и translation
    if user_translation == translation.lower():
        bot.send_message(message.chat.id, "Правильно! Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильный перевод: {translation}")

    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_number - 1)



@bot.message_handler(commands=['addword']) # /addword apple яблоко
def handle_addword(message):
    global user_data
    logging.info(f"Сообщение {message.text}")
    # bot.send_message(message.chat.id, "Добавляем новое слово")
    chat_id = str(message.chat.id)
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
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5) 
