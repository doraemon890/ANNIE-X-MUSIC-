
import telebot
import re
from config import BOT_TOKEN

# Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
bot = telebot.TeleBot(BOT_TOKEN)

# Define a function to check for copyrighted content in messages
def check_copyright(message):
    copyrighted_keywords = ["NCERT", "XII", "page", "Ans", "meiotic", "divisions", "System.in", "Scanner", "void", "nextInt"]
    for keyword in copyrighted_keywords:
        if re.search(keyword, message, re.IGNORECASE):
            return True
    return False

# Define a handler for incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if check_copyright(message.text):
        bot.reply_to(message, "This message contains copyrighted content. Please refrain from sharing copyrighted material.")
        # Delete the message containing copyrighted content
        bot.delete_message(message.chat.id, message.message_id)

# Start the bot
bot.polling()
