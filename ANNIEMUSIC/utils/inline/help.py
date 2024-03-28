from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ANNIEMUSIC import app

def generate_buttons(start_index, end_index, callback_prefix):
    buttons = []
    for i in range(start_index, end_index):
        buttons.append(InlineKeyboardButton(text=f"H_B_{i}", callback_data=f"help_callback hb{i}"))
    return buttons

def generate_page(buttons, control_button):
    page_markup = InlineKeyboardMarkup(buttons + [control_button])
    return page_markup

def first_page(_):
    controll_button = [InlineKeyboardButton(text="๏ ᴍᴇɴᴜ ๏", callback_data=f"settingsback_helper"), InlineKeyboardButton(text="๏ ɴᴇxᴛ ๏", callback_data=f"AYUSHI")]
    buttons = [
        generate_buttons(1, 16, "help_callback hb"),
    ]
    return generate_page(buttons, controll_button)

def second_page(_):
    controll_button = [InlineKeyboardButton(text="๏ ʙᴀᴄᴋ ๏", callback_data=f"settings_back_helper")]
    buttons = [
        generate_buttons(16, 31, "help_callback hb"),
    ]
    return generate_page(buttons, controll_button)

def third_page(_):
    controll_button = [InlineKeyboardButton(text="๏ ʙᴀᴄᴋ ๏", callback_data=f"settings_back_helper")]
    buttons = [
        generate_buttons(31, 46, "help_callback hb"),
    ]
    return generate_page(buttons, controll_button)

def help_pannel(_, START: Union[bool, int] = None):
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close")]
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(
            text=_["CLOSEMENU_BUTTON"], callback_data=f"close"
	),
    ]
    mark = second if START else first
    buttons = [
        generate_buttons(1, 16, "help_callback hb"),
        generate_buttons(16, 31, "help_callback hb"),
        generate_buttons(31, 46, "help_callback hb"),
        mark
    ]
    return generate_page(buttons, [])

def help_back_markup(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"settings_back_helper",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data=f"close"
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="💗 ʜᴇʟᴘ 💗",
                callback_data="settings_back_helper",
            ),
        ],
    ]
    return buttons
