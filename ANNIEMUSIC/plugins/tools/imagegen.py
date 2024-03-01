import time
from pyrogram import ChatAction
from pyrogram import filters
from ANNIEMUSIC import app
from pyrogram.types import Message
import openai
from PIL import Image, ImageDraw, ImageFont
import requests


openai.api_key = config.GPT_API

@app.on_message(filters.command(["getdraw"], prefixes=["+", ".", "/", "!"]))
async def chat(app, message: Message):
    try:
        start_time = time.time()
        await app.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        if len(message.command) < 2:
            await message.reply_text(
                "**ʜᴇʟʟᴏ sɪʀ ɪ ᴀᴍ ᴊᴀʀᴠɪs & \nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏᴅᴀʏ**")
        else:
            a = message.text.split(' ', 1)[1]
            MODEL = "text-davinci-003"
            resp = openai.ChatCompletion.create(
                model=MODEL,
                messages=[{"role": "user", "content": a}],
                max_tokens=50
            )
            image_text = resp.choices[0].message['content']
            image = generate_image(image_text)
            await app.send_photo(chat_id=message.chat.id, photo=image)
        
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")

def generate_image(text, image_size=(400, 200)):
    response = openai.Image.create(
        engine="davinci",
        prompt=text,
        max_images=1,
        temperature=0.7
    )

    image_url = response['images'][0]['url']
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))

    return image
