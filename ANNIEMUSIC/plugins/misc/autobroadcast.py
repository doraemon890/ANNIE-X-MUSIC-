import asyncio
import datetime
from ANNIEMUSIC import app
from pyrogram import Client
from ANNIEMUSIC.utils.database import get_served_chats
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


MESSAGE = f"""**💗  ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs ᴛᴏ ᴀʟʟ 💗

'([ᴀɴɴɪᴇ ᴍᴜsɪᴄ + ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʀᴏʙᴏᴛ](https://t.me/Annie_X_music_bot))'   
                    
                        '([ᴜsᴇʀs](tg://settings/))' 

❥ ᴏᴜʀ ᴀɴɴɪᴇ ᴍᴜsɪᴄ ʀᴏʙᴏᴛ ʜᴀs ʀᴇᴀᴄʜᴇᴅ  ᴀ ᴍɪʟᴇsᴛᴏɴᴇ ᴏғ ᴄᴏᴍᴘʟᴇᴛɪɴɢ ᴏᴠᴇʀ 𝟻𝟶𝟶 ᴄʜᴀᴛs.🌷 

❥ ᴛʜᴀɴᴋ ʏᴏᴜ ♔ ғᴏʀ ʏᴏᴜʀ ᴄᴏɴᴛɪɴᴜᴇᴅ sᴜᴘᴘᴏʀᴛ ᴀɴᴅ ᴇɴɢᴀɢᴇᴍᴇɴᴛ ᴡɪᴛʜ ᴏᴜʀ ɪɴɴᴏᴠᴀᴛɪᴠᴇ ᴍᴜsɪᴄ + ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʀᴏʙᴏᴛ . 🥀

❥ ʟᴇᴛ's ᴋᴇᴇᴘ ᴛʜᴇ ᴄᴇʟᴇʙʀᴀᴛɪᴏɴ ɢᴏɪɴɢ ᴀs ᴡᴇ ʟᴏᴏᴋ ғᴏʀᴡᴀʀᴅ ᴛᴏ ᴍᴀɴʏ ᴍᴏʀᴇ ᴇxᴄɪᴛɪɴɢ ɪɴᴛᴇʀᴀᴄᴛɪᴏɴs ᴡɪᴛʜ ᴀɴɴɪᴇ ʀᴏʙᴏᴛ ɪɴ ᴛʜᴇ ғᴜᴛᴜʀᴇ ! 🦋

       ([🌷 sᴜᴘᴘᴏʀᴛ 🌷](https://t.me/+143OoX4JfpQ3OGNl))      ([🎟 sᴛᴀᴛs 🎟](https://t.me/CDX_WORLD/14))  """

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")
        ]
    ]
)


CELEBRATION_VID_URL = "https://github.com/doraemon890/ANNIE-X-MUSIC-/assets/155803358/4671acf4-d356-4698-baad-43ef62438437"


async def send_message_to_chats():
    try:
        chats = await get_served_chats()

        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    await app.send_video(chat_id, video=CELEBRATION_VID_URL, caption=MESSAGE, reply_markup=BUTTON)
                    await asyncio.sleep(3)  # Sleep for 1 second between sending messages
                except Exception as e:
                    pass  # Do nothing if an error occurs while sending message
    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats
async def continuous_broadcast():
    while True:
        await send_message_to_chats()
        await asyncio.sleep(180000)  # Sleep (180000 seconds) between next broadcast

# Start the continuous broadcast loop
asyncio.create_task(continuous_broadcast())
