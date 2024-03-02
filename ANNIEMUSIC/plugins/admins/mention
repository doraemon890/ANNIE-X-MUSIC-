from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from ANNIEMUSIC import app



spam_chats = []


@app.on_message(filters.command(["tagall", "all"]) | filters.regex(r"^@all") & filters.group)
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        return await message.reply("__ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ʙᴇ ᴜꜱᴇ ɪɴ ɢʀᴏᴜᴘꜱ ʙᴀʙʏ🥀!__")

    is_admin = False
    admins = await client.get_chat_members(chat_id, filter="administrators")
    for admin in admins:
        if admin.user.id == message.from_user.id:
            is_admin = True
            break

    if not is_admin:
        return await message.reply("__ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴍᴇɴᴛɪᴏɴ ᴀʟʟ ʙᴀʙʏ🥀!__")

    mode = "text_on_cmd"
    msg = message.text.split(maxsplit=1)
    if len(msg) == 1:
        msg = ""
    else:
        msg = msg[1]

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for member in client.iter_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if member.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"@{member.user.username} "
        if usrnum == 5:
            txt = f"{msg}\n{usrtxt}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command("cancel") & filters.group)
async def cancel_spam(client, message):
    chat_id = message.chat.id
    is_admin = False
    admins = await client.get_chat_members(chat_id, filter="administrators")
    for admin in admins:
        if admin.user.id == message.from_user.id:
            is_admin = True
            break

    if not is_admin:
        return await message.reply("__ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ🥀!__")
    if not chat_id in spam_chats:
        return await message.reply("__ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ᴘʀᴏᴄᴄᴇꜱꜱ ᴏɴ ɢᴏɪɴɢ ʙᴀʙʏ🥀...__")
    else:
        try:
            spam_chats.remove(chat_id)
        except:
            pass
        return await message.reply("__ꜱᴛᴏᴘᴘᴇᴅ ᴍᴇɴᴛɪᴏɴ ʙᴀʙʏ🥀.__")
