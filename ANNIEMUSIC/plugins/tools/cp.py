from ANNIEMUSIC import ANNIEMUSIC as app
from pyrogram import Client, filters

async def delete_messages(message):
    if any(link in message.text for link in ["http", "https", "www."]):
        await message.delete()
    elif any(keyword in message.text for keyword in keywords_to_delete) and len(message.text.split()) > 20:
        await message.delete()
    elif len(message.text.split()) >= 20:
        await message.delete()

keywords_to_delete = ["NCERT", "XII", "page", "Ans", "meiotic", "divisions", "System.in", "Scanner", "void", "nextInt"]

@app.on_message(filters.group & filters.text & ~filters.me)
async def handle_messages(client, message):
    await delete_messages(message)

@app.on_edited_message(filters.group & filters.text & ~filters.me)
async def handle_edited_messages(client, edited_message):
    await delete_messages(edited_message)
