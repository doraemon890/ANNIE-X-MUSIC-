from pyrogram import Client, filters, types as t
from lexica import Client as ApiClient, AsyncClient
from pyrogram.types import InlineKeyboardButton
from math import ceil
import asyncio
from ANNIEMUSIC import app


async def ImageGeneration(client, model, prompt):
    try:
        output = await client.generate(model, prompt, "")
        if output['code'] != 1:
            return 2
        elif output['code'] == 69:
            return output['code']
        
        task_id, request_id = output['task_id'], output['request_id']
        await asyncio.sleep(20)  # You may adjust this sleep time as needed
        
        # Polling for image generation status asynchronously
        tries = 0
        while tries < 15:
            resp = await client.getImages(task_id, request_id)
            if resp['code'] == 2:
                return resp['img_urls']
            await asyncio.sleep(5)
            tries += 1
        
        return None  # Timeout, image generation failed
    
    except Exception as e:
        raise Exception(f"Failed to generate the image: {e}")


async def generate_images_concurrently(client, model, prompt):
    tasks = [ImageGeneration(client, model, prompt) for _ in range(3)]  # Adjust concurrency level as needed
    return await asyncio.gather(*tasks)


@app.on_message(filters.command(["draw", "create", "imagine", "dream"]))
async def draw(_: app, m: t.Message):
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("<code>Please provide a prompt. Usage: /draw <prompt></code>")
    
    user = m.from_user
    data = {'prompt': prompt, 'reply_to_id': m.message_id}
    Database[user.id] = data
    
    btns = paginate_models(0, Models, user.id)
    await m.reply_text(
        text=f"**Hello {m.from_user.mention}**\n\n**Select your image generator model**",
        reply_markup=t.InlineKeyboardMarkup(btns)
    )


@app.on_callback_query(filters.regex(pattern=r"^d.(.*)"))
async def selectModel(_: app, query: t.CallbackQuery):
    data = query.data.split('.')
    auth_user = int(data[-1])
    if query.from_user.id != auth_user:
        return await query.answer("No.")
    
    if len(data) > 3:
        if data[1] == "right":
            next_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(next_page + 1, Models, auth_user)
                )
            )
        elif data[1] == "left":
            curr_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(curr_page - 1, Models, auth_user)
                )
            )
        return
    
    modelId = int(data[1])
    await query.edit_message_text("**Please wait, generating your image.**")
    
    promptData = Database.get(auth_user, None)
    if promptData is None:
        return await query.edit_message_text("Something went wrong.")
    
    async with AsyncClient() as client:
        img_urls = await generate_images_concurrently(client, modelId, promptData['prompt'])
    
    if img_urls is None or img_urls == 2 or img_urls == 1:
        return await query.edit_message_text("Something went wrong.")
    
    elif img_urls == 69:
        return await query.edit_message_text("NSFW not allowed!")
    
    images = [t.InputMediaPhoto(img_url) for img_url in img_urls]
    images[-1] = t.InputMediaPhoto(img_urls[-1], caption=f"Your Prompt:\n`{promptData['prompt']}`")
    
    await query.message.delete()
    try:
        del Database[auth_user]
    except KeyError:
        pass
    
    await _.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=promptData['reply_to_id']
    )


def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


class AnInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_models(page_n: int, models: list, user_id) -> list:
    modules = sorted(
        [
            AnInlineKeyboardButton(
                x['name'],
                callback_data=f"d.{x['id']}.{user_id}"
            )
            for x in models
        ]
    )

    pairs = list(zip(modules[::3], modules[1::3]))
    i = sum(len(m) for m in pairs)
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 3

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
                modulo_page * COLUMN_SIZE: COLUMN_SIZE * (modulo_page + 1)
                ] + [
                    (
                        AnInlineKeyboardButton(
                            "◁",
                            callback_data=f"d.left.{modulo_page}.{user_id}"
                        ),
                        AnInlineKeyboardButton(
                            "⌯ Cancel ⌯",
                            callback_data=f"close_data"
                        ),
                        AnInlineKeyboardButton(
                            "▷",
                            callback_data=f"d.right.{modulo_page}.{user_id}"
                        ),
                    )
                ]
    else:
        pairs += [[AnInlineKeyboardButton("⌯ Back ⌯", callback_data=f"d.-1.{user_id}")]]

    return pairs
