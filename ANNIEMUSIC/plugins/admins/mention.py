import asyncio
from pyrogram import filters
from ANNIEMUSIC import app
from ANNIEMUSIC.utils.jarvis_ban import admin_filter

SPAM_CHATS = []

@app.on_message(filters.command(["mention", "all"]) & filters.group & admin_filter)
async def tag_all_users(_, message):
    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ**")
        return
    if replied:
        SPAM_CHATS.append(message.chat.id)
        print(f"Added chat_id {message.chat.id} to SPAM_CHATS")  # Add this line
        usernum = 0
        usertxt = ""
        async for m in app.iter_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"\n⊚ [{m.user.first_name}](tg://user?id={m.user.id})"
            if usernum % 5 == 0:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usertxt = ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]
        SPAM_CHATS.append(message.chat.id)
        print(f"Added chat_id {message.chat.id} to SPAM_CHATS")  # Add this line
        usernum = 0
        usertxt = ""
        async for m in app.iter_chat_members(message.chat.id):
            if message.chat.id not in SPAM_CHATS:
                break
            usernum += 1
            usertxt += f"\n⊚ [{m.user.first_name}](tg://user?id={m.user.id})"
            if usernum % 5 == 0:
                await app.send_message(message.chat.id, f'{text}\n{usertxt}')
                await asyncio.sleep(2)
                usertxt = ""
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass

@app.on_message(filters.command(["alloff", "cancel"]) & ~filters.private)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
            print(f"Removed chat_id {chat_id} from SPAM_CHATS")  # Add this line
        except Exception as e:
            print(f"Error removing chat_id from SPAM_CHATS: {e}")
    pass 
        return await message.reply_text("**🦋ᴛᴀɢ ʀᴏᴋɴᴇ ᴡᴀʟᴇ ᴋɪ ᴍᴀᴀ ᴋᴀ ʙʜᴀʀᴏsᴀ ᴊᴇᴇᴛᴜ.....🫠!**")
    else:
        await message.reply_text("**No ongoing process!**")
