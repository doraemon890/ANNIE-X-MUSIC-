from pyrogram.types import InlineKeyboardButton

import config
from ANNIEMUSIC import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["✧ ᴀᴅᴅ ᴍᴇ ✧"], url=f"https://t.me/{app.username}?startgroup=true")
        ],
        [
            InlineKeyboardButton(text="✨ sᴜᴩᴩᴏʀᴛ ✨", url="https://t.me/JARVIS_X_SUPPORT"),
            InlineKeyboardButton(text="🥀 ᴅᴇᴠᴇʟᴏᴩᴇʀ 🥀", url=config.OWNER_ID)
        ],
    ]
    return buttons



def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_10"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper"),
        ],
    ]
    return buttons
