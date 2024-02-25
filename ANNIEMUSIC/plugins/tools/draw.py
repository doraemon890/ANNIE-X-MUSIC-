from pyrogram import Client, filters, types as t
from lexica import Client as ApiClient, AsyncClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from math import ceil
import asyncio
from ANNIEMUSIC import app

api = ApiClient()
Models = api.getModels()['models']['image']
Database = {}

async def generate_image(model, prompt):
    try:
        client = AsyncClient()
        output = await client.generate(model, prompt, "")
        if output.get('code') != 1:
            return None
        task_id, request_id = output['task_id'], output['request_id']
        await asyncio.sleep(20)
        tries = 0
        image_url = None
        resp = await client.getImages(task_id, request_id)
        while resp.get('code') != 2 and tries <= 15:
            await asyncio.sleep(5)
            resp = await client.getImages(task_id, request_id)
            tries += 1
        if resp.get('code') == 2:
            image_url = resp['img_urls']
        return image_url
    except Exception as e:
        raise Exception(f"Failed to generate the image: {e}")
    finally:
        await client.close()

def get_text(message):
    """Extract Text From Commands"""
    text_to_return = message.text
    if text_to_return is None or " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None

class AnInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text
    def __lt__(self, other):
        return self.text < other.text
    def __gt__(self, other):
        return self.text > other.text

def paginate_models(page_n: int, models: list, user_id) -> list:
    modules = sorted([
        AnInlineKeyboardButton(x['name'], callback_data=f"d.{x['id']}.{user_id}")
        for x in models
    ])
    pairs = list(zip(modules[::3], modules[1::3]))
    i = sum(1 for _ in sum(pairs, ()))
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append((modules[-2], modules[-1]))
    COLUMN_SIZE = 3
    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages
    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE: COLUMN_SIZE * (modulo_page + 1)] + [
            (
                AnInlineKeyboardButton("◁", callback_data=f"d.left.{modulo_page}.{user_id}"),
                AnInlineKeyboardButton("⌯ ᴄᴀɴᴄᴇʟ ⌯", callback_data="close_data"),
                AnInlineKeyboardButton("▷", callback_data=f"d.right.{modulo_page}.{user_id}")
            )
        ]
    else:
        pairs += [[AnInlineKeyboardButton("⌯ ʙᴀᴄᴋ ⌯", callback_data=f"d.-1.{user_id}")]]
    return pairs

# The remaining code for message handling and callback queries remains the same

app = Client("my_bot")

@app.on_message(filters.command(["draw","create","imagine","dream"]))
async def draw(_, m: t.Message):
    global Database
    prompt = get_text(m)
    if prompt is None:
        return await m.reply_text("<code>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ. ᴜsᴀɢᴇ: /draw <prompt></code>")
    user = m.from_user
    data = {'prompt': prompt, 'reply_to_id': m.message_id}
    Database[user.id] = data
    btns = paginate_models(0, Models, user.id)
    await m.reply_text(
        text=f"**ʜᴇʟʟᴏ {m.from_user.mention}**\n\n**sᴇʟᴇᴄᴛ ʏᴏᴜʀ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛᴏʀ ᴍᴏᴅᴇʟ**",
        reply_markup=InlineKeyboardMarkup(btns)
    )

@app.on_callback_query(filters.regex(pattern=r"^d.(.*)"))
async def select_model(_, query: t.CallbackQuery):
    global Database
    data = query.data.split('.')
    auth_user = int(data[-1])
    if query.from_user.id != auth_user:
        return await query.answer("No.")
    if len(data) > 3:
        if data[1] == "right":
            next_page = int(data[2])
            await query.edit_message_reply_markup(
                InlineKeyboardMarkup(paginate_models(next_page + 1, Models, auth_user))
            )
        elif data[1] == "left":
            curr_page = int(data[2])
            await query.edit_message_reply_markup(
                InlineKeyboardMarkup(paginate_models(curr_page - 1, Models, auth_user))
            )
        return
    model_id = int(data[1])
    await query.edit_message_text("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ, ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ ɪᴍᴀɢᴇ.**")
    prompt_data = Database.get(auth_user, None)
    if prompt_data is None:
        return await query.edit_message_text("Something went wrong.")
    img_url = await generate_image(model_id, prompt_data['prompt'])
    if img_url is None:
        return await query.edit_message_text("Something went wrong.")
    images = [InputMediaPhoto(img_url[-1], caption=f"Your Prompt:\n`{prompt_data['prompt']}`")]
    await query.message.delete()
    try:
        del Database[auth_user]
    except KeyError:
        pass
    await _.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=prompt_data['reply_to_id']
    )
