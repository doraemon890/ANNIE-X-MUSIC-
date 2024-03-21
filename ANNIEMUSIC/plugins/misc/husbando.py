from pyrogram import Client, filters
import requests
from ANNIEMUSIC import app
import html

# Function to retrieve husbando information from the API
def get_husbando_info(api_token):
    url = "https://waifu.it/api/v4/husbando"
    headers = {
        "Authorization": api_token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

# Function to retrieve waifu information from the API
def get_waifu_info(api_token):
    url = "https://waifu.it/api/v4/waifu"
    headers = {
        "Authorization": api_token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

# Command handler for /husbando command
@app.on_message(filters.command("husbando") & ~filters.forwarded & ~filters.via_bot)
def husbando_command(client, message):
    try:
        # Replace "YOUR_HUSBANDO_TOKEN" with your actual API token obtained from Kohai Bot
        api_token = "MTIyMDIyOTIxNjQ4Mjg4OTc0OA--.MTcxMDk5NTgxMA--.fb82de684cd7"
        husbando_data = get_husbando_info(api_token)

        if husbando_data:
            # Format and send husbando information
            msg = format_data(husbando_data)
            message.reply_text(msg, parse_mode='html')
        else:
            message.reply_text("Couldn't retrieve the husbando data. Please try again.")
        
    except Exception as e:
        message.reply_text(f"An unexpected error occurred: {str(e)}")

# Command handler for /waifu command
@app.on_message(filters.command("waifu") & ~filters.forwarded & ~filters.via_bot)
def waifu_command(client, message):
    try:
        # Replace "YOUR_WAIFU_TOKEN" with your actual API token obtained from Kohai Bot
        api_token = "MTIyMDIyOTIxNjQ4Mjg4OTc0OA--.MTcxMDk5NTgxMA--.fb82de684cd7"
        waifu_data = get_waifu_info(api_token)

        if waifu_data:
            # Format and send waifu information
            msg = format_data(waifu_data)
            message.reply_text(msg, parse_mode='html')
        else:
            message.reply_text("Couldn't retrieve the waifu data. Please try again.")
        
    except Exception as e:
        message.reply_text(f"An unexpected error occurred: {str(e)}")

# Function to format husbando or waifu data
def format_data(data):
    msg = f"<b>{'Husbando' if 'husbando' in data['name'] else 'Waifu'} Info</b>:\n\n"
    msg += f"<b>_id:</b> {data.get('_id')}<br/>"
    msg += f"<b>Name:</b> {html.escape(data.get('name')['userPreferred'])}<br/>"
    msg += f"<b>Image:</b> {data.get('image')['large']}<br/>"
    msg += f"<b>Description:</b> {html.escape(data.get('description'))}<br/>"
    msg += f"<b>Age:</b> {data.get('age')}<br/>"
    msg += f"<b>Gender:</b> {data.get('gender')}<br/>"
    msg += f"<b>Blood Type:</b> {data.get('bloodType')}<br/>"
    msg += f"<b>Date of Birth:</b> {data.get('dateOfBirth')['year']}-{data.get('dateOfBirth')['month']}-{data.get('dateOfBirth')['day']}<br/>"
    msg += "<b>Media Nodes:</b><br/>"
    for node in data.get('media', {}).get('nodes', []):
        msg += f"- <b>Title:</b> {html.escape(node.get('title')['userPreferred'])}<br/>"
        msg += f"  <b>Type:</b> {node.get('type')}<br/>"
        msg += f"  <b>Format:</b> {node.get('format')}<br/>"
    return msg
