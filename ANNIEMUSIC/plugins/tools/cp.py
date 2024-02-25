from pyrogram import Client, filters
import logging


app = Client("@Annie_X_music_bot")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

FORBIDDEN_KEYWORDS = ["porn", "xxx", "sex", "NCERT", "XII", "page", "Ans", "meiotic", "divisions", "System.in", "Scanner", "void", "nextInt"]

# Handler for all messages
@app.on_message(filters.text | filters.caption)
async def handle_message(client, message):
    try:
        if any(keyword in message.text.lower() for keyword in FORBIDDEN_KEYWORDS):
            logging.info(f"Deleting message with ID {message.message_id}")
            await message.delete()
            await message.reply_text(f"@{message.from_user.username} Don't send inappropriate messages!")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Function to check message length
def is_long_message(_, message):
    return len(message.text.split()) > 10

# Handler to delete long messages and notify the user
@app.on_message(filters.group & filters.private & is_long_message)
async def delete_long_messages(_, message):
    try:
        await message.delete()
        await message.reply_text("Please keep your messages short!")
    except Exception as e:
        logging.error(f"An error occurred while deleting message: {e}")

