import telebot
from config import api_token

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это бот для изучения английского языка")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "У меня пока нет имени")
    elif message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "Я бот для изучения английского языка")

if __name__ == "__main__":
    bot.polling(non_stop=True)