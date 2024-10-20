import telebot
from config import api_token


TOKEN = api_token

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Бот для записи на процедуры запущен.")


if __name__ == "__main__":
    bot.polling(none_stop=True)