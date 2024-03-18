import base64
import os
import requests
from uuid import uuid4
import aiohttp
import httpx
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ANNIEMUSIC import app
import pyrogram


@app.on_message(filters.reply & filters.command(["upscale"]))
async def upscale_image(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text("**ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ ᴛᴏ ᴜᴘsᴄᴀʟᴇ ɪᴛ.**")
            return

        image = message.reply_to_message.photo.file_id
        file_path = await client.download_media(image)

        with open(file_path, "rb") as image_file:
            f = image_file.read()

        b = base64.b64encode(f).decode("utf-8")

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "https://api.qewertyy.me/upscale", data={"image_data": b}, timeout=None
            )

        with open("upscaled_image.png", "wb") as output_file:
            output_file.write(response.content)

        await client.send_document(
            message.chat.id,
            document="upscaled_image.png",
            caption="**ʜᴇʀᴇ ɪs ᴛʜᴇ ᴜᴘsᴄᴀʟᴇᴅ ɪᴍᴀɢᴇ!**",
        )

    except Exception as e:
        print(f"**ғᴀɪʟᴇᴅ ᴛᴏ ᴜᴘsᴄᴀʟᴇ ᴛʜᴇ ɪᴍᴀɢᴇ**: {e}")
        await message.reply_text("**ғᴀɪʟᴇᴅ ᴛᴏ ᴜᴘsᴄᴀʟᴇ ᴛʜᴇ ɪᴍᴀɢᴇ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ**.")

# Waifu image functionality
@app.on_message(filters.command("waifu"))
async def waifu_command_handler(_, message):
    try:
        tags = ['maid']  # You can customize the tags as needed
        waifu_data = get_waifu_data(tags)

        if waifu_data and 'images' in waifu_data:
            first_image = waifu_data['images'][0]
            image_url = first_image['url']
            await message.reply_photo(image_url)
        else:
            await message.reply_text("No waifu found with the specified tags.")

    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply_text(f"An error occurred: {e}")

# Helper function to get waifu data
def get_waifu_data(tags):
    params = {
        'included_tags': tags,
        'height': '>=2000'
    }

    response = requests.get('https://api.waifu.im/search', params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None
