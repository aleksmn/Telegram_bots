import telebot
import json
import logging
from datetime import date, time, datetime, timedelta

from config import api_token


# d = date.today()
# dt = datetime.now()
# d = date(2020, 5, 25)
# print(type(d))
# t = time(5, 30, 25)

# date1 = date(2007, 2, 4)
# date2 = date(2016, 7, 16)

# # Вычисляем разницу между датами
# date_difference = date2 - date1

# # Извлекаем количество дней из разницы
# days_diff = date_difference.days

# print(type(days_diff))



TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Бот для записи на процедуры запущен.")


@bot.message_handler(commands=['show_dates'])
def handle_schedule(message):
    """Выбор даты"""
    # Отправляем клавиатуру с кнопками

    keyboard = generate_date_schedule()
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=keyboard)


def generate_date_schedule():
    keyboard = telebot.types.InlineKeyboardMarkup()

    # Получаем кнопки для указанной даты
    days = []

    for i in range(7):
        days.append(date.today() + timedelta(days=3 + i))

    # Создаем кнопки и добавляем их на клавиатуру
    for button_text in days:
        callback_data = f"day:{button_text}"
        button = telebot.types.InlineKeyboardButton(text=f"{button_text}", callback_data=callback_data)
        keyboard.add(button)

    return keyboard


# Функция для генерации клавиатуры с временем
def generate_time_keyboard(chosen_date):
    keyboard = telebot.types.InlineKeyboardMarkup()

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
        button = telebot.types.InlineKeyboardButton(text=time, callback_data=callback_data)
        keyboard.add(button)

    return keyboard


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data.startswith("day:"):
        chosen_date = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали дату: {chosen_date}")

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