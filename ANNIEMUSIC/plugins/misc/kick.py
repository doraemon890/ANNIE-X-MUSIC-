from pyrogram import Client, filters
import requests
from ANNIEMUSIC import app

# Function to retrieve kick animation URL from the API
def get_kick_animation(api_token):
    url = "https://waifu.it/api/v4/kick"
    headers = {
        "Authorization": api_token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("url")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

# Command handler for /kick command
@app.on_message(filters.command("kik") & ~filters.forwarded & ~filters.via_bot)
def kick_command(client, message):
    try:
        sender = message.from_user.mention(style='markdown')
        target = sender if not message.reply_to_message else message.reply_to_message.from_user.mention(style='markdown')
        
        # Replace "Your-API-Token" with your actual API token
        api_token = "MTIyMDIyOTIxNjQ4Mjg4OTc0OA--.MTcxMDk5NTgxMA--.fb82de684cd7"
        gif_url = get_kick_animation(api_token)

        if gif_url:
            msg = f"{sender} kicked {target}! 😠"
            message.reply_animation(animation=gif_url, caption=msg)
        else:
            message.reply_text("Couldn't retrieve the animation. Please try again.")
        
    except Exception as e:
        message.reply_text(f"An unexpected error occurred: {str(e)}")
