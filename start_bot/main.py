import telebot
from config import api_token


# pip install pyTelegramBotAPI


TOKEN = api_token

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот!")


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.polling(non_stop=True)