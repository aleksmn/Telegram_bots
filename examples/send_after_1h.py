import telebot
import time
import threading

TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'  # Replace with your chat ID

bot = telebot.TeleBot(TOKEN)

def send_message_after_delay(message, delay):
    time.sleep(delay)  # Delay in seconds
    bot.send_message(chat_id=CHAT_ID, text=message)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Bot started! I will send a message in 1 hour.")
    delay = 3600  # 1 hour in seconds
    threading.Thread(target=send_message_after_delay, args=("Hello! This message is sent after 1 hour.", delay)).start()

if __name__ == "__main__":
    print("Bot is polling...")
    bot.polling(none_stop=True)
