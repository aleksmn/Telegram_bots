import json
import random

import telebot

from config import api_token

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот.")


# Обработка команды /learn
@bot.message_handler(commands=['learn'])
def handle_learn(message):
    user_words = user_data.get(str(message.chat.id), {})

    # Проверяем, есть ли у пользователя слова для изучения
    if not user_words:
        bot.send_message(message.chat.id, "Твой словарь пуст! Добавь слова с помощью команды /addword.")
        return

    try:
        words_number = int(message.text.split()[1])
        # Начинаем процесс изучения
        ask_translation(message.chat.id, user_words, words_number)
    except ValueError:
        bot.send_message(message.chat.id, "Используй команду /learn <количество> для изучения слов.")
    except IndexError:
        bot.send_message(message.chat.id, "Используй команду /learn <количество> для изучения слов.")


# ДОБАВЛЕНА ФУНКЦИЯ
def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова '{word}'.")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, "Урок закончен")


# ДОБАВЛЕНА ФУНКЦИЯ
def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, "Правильно! Молодец!")
    else:
        bot.send_message(message.chat.id, f"Неправильно. Правильный перевод: {expected_translation}")

    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left - 1)


@bot.message_handler(commands=["addword"])  # /addword apple яблоко
def handle_addword(message):
    global user_data
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
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова")


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Я бот для изучения английского языка.")
    bot.send_message(message.chat.id, "Вот список доступных команд:")
    bot.send_message(message.chat.id, "/start - Начало работы с ботом")
    bot.send_message(message.chat.id, "/learn - Начать обучение")
    bot.send_message(message.chat.id, "/help - Посмотреть справку")
    bot.send_message(message.chat.id, "Автор бота: Ваше Имя")


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
    bot.polling(none_stop=True)