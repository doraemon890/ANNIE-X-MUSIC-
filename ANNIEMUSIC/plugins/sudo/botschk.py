import asyncio
from pyrogram import filters
from ANNIEMUSIC import app, userbot
from config import OWNER_ID

BOT_LIST = ["Annie_X_music_bot"]

@app.on_message(filters.command("botschk") & filters.user(OWNER_ID))
async def bots_chk(_, message):
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
                    response += f"🟢 [{bot.first_name}](tg://user?id={bot.id}) - **sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ ✨**\n\n"
                else:
                    response += f"🔴 [{bot.first_name}](tg://user?id={bot.id}) - **sᴛᴀᴛᴜs: ᴏғғʟɪɴᴇ ❄**\n\n"
        except Exception as e:
            response += f"❌ {bot_username} - **sᴛᴀᴛᴜs: ᴇʀʀᴏʀ ({str(e)})**\n\n"
    
    await msg.edit_text(response)

@app.on_message(filters.command("addbot") & filters.user(OWNER_ID))
async def add_bot(_, message):
    bruh = message.text.split(maxsplit=1)[1]
    add_bots = bruh.split()
    response = "Successfully added bots to the bot checker list\n\n"
    msg = await message.reply("Please wait...")
    
    for i in add_bots:
        if i not in BOT_LIST:
            BOT_LIST.append(i)
            response += f"{i} Added.\n\n"
        else:
            response += f"{i} Already added.\n\n"
    await msg.edit_text(response)

@app.on_message(filters.command("rmbot") & filters.user(OWNER_ID))
async def remove_bot(_, message):
    bruh = message.text.split(maxsplit=1)[1]
    remove_bots = bruh.split()
    response = "Successfully removed bots from the bot list\n\n"
    msg = await message.reply("Removing bots...")
    
    for i in remove_bots:
        if i in BOT_LIST:
            BOT_LIST.remove(i)
            response += f"{i} Removed.\n\n"
        else:
            response += f"{i} Not found in the list.\n\n"

    await msg.edit_text(response)
