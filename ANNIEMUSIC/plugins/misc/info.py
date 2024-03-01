import asyncio
import os
import aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters, Client, enums
from pyrogram.types import *
from typing import Union, Optional
import random
from ANNIEMUSIC import app
anniephoto = [
    "https://telegra.ph/file/07fd9e0e34bc84356f30d.jpg",
    "https://telegra.ph/file/3c4de59511e179018f902.jpg",
    "https://telegra.ph/file/07fd9e0e34bc84356f30d.jpg",
    "https://telegra.ph/file/3c4de59511e179018f902.jpg",
    "https://telegra.ph/file/002b98f44394097758551.jpg"
]

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = lambda text_size, text: (text[:text_size] + "...").upper() if len(text) > text_size else text.upper()

async def get_userinfo_img(bg_path: str, font_path: str, user_id: Union[int, str], profile_path: Optional[str] = None):
    bg = Image.open(bg_path)
    
    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)
        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((833, 857))
        bg.paste(resized, (1029, 67), resized)
    
    img_draw = ImageDraw.Draw(bg)
    img_draw.text((2405, 720), text=str(user_id).upper(), font=get_font(95, font_path), fill=(125, 227, 230))
    
    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    
    return path

bg_path = "ANNIEMUSIC/assets/annie/jarvisXinfo.png"
font_path = "ANNIEMUSIC/assets/annie/jarvisinf.ttf"

INFO_TEXT = """
**❅─────✧❅✦❅✧─────❅
            ✦ ᴜsᴇʀ ɪɴғᴏ ✦
➻ ᴜsᴇʀ ɪᴅ ‣ **`{}`
**➻ ғɪʀsᴛ ɴᴀᴍᴇ ‣ **{}
**➻ ʟᴀsᴛ ɴᴀᴍᴇ ‣ **{}
**➻ ᴜsᴇʀɴᴀᴍᴇ ‣ **`{}`
**➻ ᴍᴇɴᴛɪᴏɴ ‣ **{}
**➻ ʟᴀsᴛ sᴇᴇɴ ‣ **{}
**➻ ᴅᴄ ɪᴅ ‣ **{}
**➻ ʙɪᴏ ‣ **`{}`
**❅─────✧❅✦❅✧─────❅**
"""

async def get_user_status(user_id):
    try:
        user = await app.get_users(user_id)
        status = user.status
        
        if status == enums.UserStatus.RECENTLY:
            return "Recently."
        elif status == enums.UserStatus.LAST_WEEK:
            return "Last week."
        elif status == enums.UserStatus.LONG_AGO:
            return "Long time ago."
        elif status == enums.UserStatus.OFFLINE:
            return "Offline."
        elif status == enums.UserStatus.ONLINE:
            return "Online."
    except Exception as e:
        print(f"Error getting user status: {e}")
        return "**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ !**"

@app.on_message(filters.command(["info", "userinfo"], prefixes=["/", "!", "."]))
async def userinfo(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    reply_message = message.reply_to_message
    msg = await message.reply_text("💻")
    await asyncio.sleep(2)
    await msg.delete()

    try:
        if not reply_message and len(message.command) == 2:
            user_id = message.text.split(None, 1)[1]
        elif reply_message:
            user_id = reply_message.from_user.id

       if not reply_message:
    user_info = await app.get_chat(user_id)
    user = await app.get_users(user_id)
    status = await get_user_status(user.id)
    id = user_info.id
    dc_id = user.dc_id
    first_name = user_info.first_name 
    last_name = user_info.last_name if user_info.last_name else "No last name"
    username = user_info.username if user_info.username else "No Username"
    mention = user.mention
    bio = user_info.bio if user_info.bio else "No bio set"

    if user.photo:
        # User has a profile photo
        photo = await app.download_media(user.photo.big_file_id)
        welcome_photo = await get_userinfo_img(
            bg_path=bg_path,
            font_path=font_path,
            user_id=user.id,
            profile_path=photo,
        )
    else:
        # User doesn't have a profile photo, use anniephoto directly
        welcome_photo = random.choice(anniephoto)

    try:
         if not reply_message:
    if len(message.command) == 2:
        user_id = message.text.split(None, 1)[1]
    else:
        # Handle the case when the command does not contain a user ID
        await message.reply_text("Please provide a user ID.")
        return
else:
    user_id = reply_message.from_user.id

try:
    user_info = await app.get_chat(user_id)
    user = await app.get_users(user_id)
    status = await get_user_status(user.id)
    id = user_info.id
    dc_id = user.dc_id
    first_name = user_info.first_name 
    last_name = user_info.last_name if user_info.last_name else "No last name"
    username = user_info.username if user_info.username else "No Username"
    mention = user.mention
    bio = user_info.bio if user_info.bio else "No bio set"

    if user.photo:
        # User has a profile photo
        photo = await app.download_media(user.photo.big_file_id)
        welcome_photo = await get_userinfo_img(
            bg_path=bg_path,
            font_path=font_path,
            user_id=user.id,
            profile_path=photo,
        )
    else:
        # User doesn't have a profile photo, use anniephoto directly
        welcome_photo = random.choice(anniephoto)

    await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
        id, first_name, last_name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
except Exception as e:
    await message.reply_text(str(e))

        await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
            id, first_name, last_name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
    except Exception as e:
        await message.reply_text(str(e))

elif reply_message:
    user_id = reply_message.from_user.id
    user_info = await app.get_chat(user_id)
    user = await app.get_users(user_id)
    status = await get_user_status(user.id)
    id = user_info.id
    dc_id = user.dc_id
    first_name = user_info.first_name 
    last_name = user_info.last_name if user_info.last_name else "No last name"
    username = user_info.username if user_info.username else "No Username"
    mention = user.mention
    bio = user_info.bio if user_info.bio else "No bio set"

    if user.photo:
        photo = await app.download_media(user.photo.big_file_id)
        welcome_photo = await get_userinfo_img(bg_path=bg_path, font_path=font_path, user_id=user.id, profile_path=photo)
    else:
        welcome_photo = random.choice(anniephoto)

    try:
        await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
            id, first_name, last_name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
    except Exception as e:
        await message.reply_text(str(e))

            if user.photo:
                # User has a profile photo
                photo = await app.download_media(user.photo.big_file_id)
                welcome_photo = await get_userinfo_img(
                    bg_path=bg_path,
                    font_path=font_path,
                    user_id=user.id,
                    profile_path=photo,
                )
            else:
                # User doesn't have a profile photo, use anniephoto directly
                welcome_photo = random.choice(anniephoto)

            await app.send_photo(chat_id, photo=welcome_photo, caption=INFO_TEXT.format(
                id, first_name, last_name, username, mention, status, dc_id, bio), reply_to_message_id=message.id)
            
    except Exception as e:
        await message.reply_text(str(e))
