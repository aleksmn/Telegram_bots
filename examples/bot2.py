import random

import telebot
from telebot import types
import json
from datetime import date, timedelta

TOKEN = ""
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=['show_dates'])
def handle_schedule(message):
    """Выбор даты"""
    # Отправляем клавиатуру с кнопками

    keyboard = generate_date_schedule()
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)


def generate_date_schedule():
    keyboard = types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты
    days = []

    for i in range(7):
        days.append(date.today() + timedelta(days=3 + i))

    # Создаем кнопки и добавляем их на клавиатуру
    for button_text in days:
        callback_data = f"day:{button_text}"
        button = types.InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard.add(button)

    return keyboard


# Функция для генерации клавиатуры с временем
def generate_time_keyboard(chosen_date):
    keyboard = types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты и времени
    times = ["10:00", "12:00", "15:00", "17:00"]

    with open("data.json", "r") as f:
        f = json.load(f)
        for appointment in f["appointments"]:
            if appointment["date"] == date:
                times.remove(appointment["time"])

    # Создаем кнопки и добавляем их на клавиатуру
    for time in times:
        callback_data = f"appointment:{chosen_date}:{time}"
        button = types.InlineKeyboardButton(text=time, callback_data=callback_data)
        keyboard.add(button)

    return keyboard


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data.startswith("day:"):
        chosen_date = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали дату: {chosen_date}")
        # Отправляем клавиатуру с доступным временем для выбранной даты
        bot.send_message(call.message.chat.id, "Выберите время:", reply_markup=generate_time_keyboard(chosen_date))

    elif call.data.startswith("appointment:"):
        chosen_date, chosen_time = call.data.split(":")[1], call.data.split(":")[2]
        add_appointment(chosen_date, chosen_time, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"Вы записаны на {chosen_date} в {chosen_time}. Ждём вас!")


def add_appointment(date, time, client):
    # Чтение существующих данных из файла
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": []}

    # Добавление новой записи
    # new_appointment = {'date': date, 'time': time, 'client': client}
    new_appointment = {'date': date.isoformat(), 'time': time, 'client': client}
    data['appointments'].append(new_appointment)

    # Запись обновленных данных в файл
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


# Обработчик команды /add_review
@bot.message_handler(commands=['add_review'])
def handle_add_review(message):
    bot.send_message(message.chat.id, "Напишите отзыв:")
    bot.register_next_step_handler(message, save_review)


# Функция для сохранения отзыва
def save_review(message):
    client_id = message.chat.id
    review_text = message.text
    # Запись отзыва в файл
    add_review(client_id, review_text)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв!")

def add_review(client, text):
    try:
        # Чтение данных из файла
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        # Если файла нет, создаем пустую структуру
        data = {"appointments": [], "review": []}

    # Добавление нового отзыва в список отзывов
    data["review"].append({
        "client": client,
        "text": text
    })

    # Сохранение обновленных данных в файл
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


@bot.message_handler(commands=['set_name'])
def handle_set_name(message):
    bot.send_message(message.chat.id, "Введите имя")
    bot.register_next_step_handler_by_chat_id(message.chat.id, lambda message: save_client(message))


def save_client(message):
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": [], "clients": {}}

    # Сохраняем имя пользователя
    data['clients'][message.chat.id] = message.text

    # Запись обновленных данных в файл
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

    bot.send_message(message.chat.id, "Ваше имя сохранено")


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)