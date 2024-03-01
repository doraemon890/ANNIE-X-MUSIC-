import time
from pyrogram import filters
from pyrogram.enums import ChatAction
from ANNIEMUSIC import app
from pyrogram.types import Message
import openai
from PIL import Image
import requests
from io import BytesIO
import config

openai.api_key = config.GPT_API

@app.on_message(filters.command(["getdraw"], prefixes=["+", ".", "/", "!"]))
async def get_draw(app, message: Message):
    try:
        start_time = time.time()
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            await message.reply_text(
                "**ʜᴇʟʟᴏ sɪʀ ɪ ᴀᴍ ᴊᴀʀᴠɪs & \nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏᴅᴀʏ**")
        else:
            a = message.text.split(' ', 1)[1]
            image = generate_image(a)
            await app.send_photo(chat_id=message.chat.id, photo=image)
        
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")

def generate_image(text, image_size=(1024, 1024)):
    openai.api_key = config.GPT_API
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )

    if 'images' not in response or len(response['images']) == 0:
        raise ValueError("Failed to generate image. No images found in response.")

    image_url = response['images'][0]['url']
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))

    return image
