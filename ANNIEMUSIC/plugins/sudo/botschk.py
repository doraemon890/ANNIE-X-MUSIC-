import asyncio
from pyrogram import filters
from ANNIEMUSIC import app, userbot
from ANNIEMUSIC.misc import SUDOERS

BOT_LIST = ["Annie_X_music_bot"]



@app.on_message(filters.command("botschk") & filters.user(SUDOERS))
async def bots_chk(app, message):
    msg = await message.reply_photo(photo="https://telegra.ph/file/e7a1c0481617facf5fb37.jpg", caption="**ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛs sᴛᴀᴛs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ...**")
    response = "**ʙᴏᴛs sᴛᴀᴛᴜs ᴅᴇᴀᴅ ᴏʀ ᴀʟɪᴠᴇ ᴄʜᴇᴄᴋᴇʀ**\n\n"
    for bot_username in BOT_LIST:
        try:
            bot = await userbot.get_users(bot_username)
            bot_id = bot.id
            await asyncio.sleep(0.5)
            bot_info = await userbot.send_message(bot_id, "/start")
            await asyncio.sleep(3)
            async for bot_message in userbot.get_chat_history(bot_id, limit=1):
                if bot_message.from_user.id == bot_id:
                    response += f"╭⎋ [{bot.first_name}](tg://user?id={bot.id})\n╰⊚ **sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ ✨**\n\n"
                else:
                    response += f"╭⎋ [{bot.first_name}](tg://user?id={bot.id})\n╰⊚ **sᴛᴀᴛᴜs: ᴏғғʟɪɴᴇ ❄**\n\n"
        except Exception:
            response += f"╭⎋ {bot_username}\n╰⊚ **sᴛᴀᴛᴜs: ᴇʀʀᴏʀ ❌**\n"
    
    await msg.edit_text(response)





@app.on_message(filters.command("addbot") & filters.user(SUDOERS))
async def add_bot(app, message):
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")
    add_bots = list(data)
    response = "successfully added bots in bots checker list\n\n"
    msg = await message.reply("wait sir...")
    
    for i in add_bots:
        if i not in BOT_LIST:
            BOT_LIST.append(i)
            response += f"{i} Added .\n\n"
        else:
            response += f"{i} Already\n\n"
    await msg.edit_text(response)



@app.on_message(filters.command("rmbot") & filters.user(SUDOERS))
async def remove_bot(app, message):
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")
    remove_bots = list(data)
    response = "successfully removed bots on the bots list\n\n"
    msg = await message.reply("wait baby...")
    
    for i in remove_bots:
        if i in BOT_LIST:
            BOT_LIST.remove(i)
            response += f"{i} Removed.\n\n"
        else:
            response += f"{i} Not in list.\n\n"

    await msg.edit_text(response)


