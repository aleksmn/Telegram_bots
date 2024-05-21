import telebot
from config import api_token

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Это твой бот!")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling(non_stop=True)