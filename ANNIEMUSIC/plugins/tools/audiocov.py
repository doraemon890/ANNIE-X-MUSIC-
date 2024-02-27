from pyrogram import Client, filters
from pydub import AudioSegment
import io
import speech_recognition as sr
from ANNIEMUSIC import app

# Function to convert audio file to text
def audio_to_text(audio_data):
    recognizer = sr.Recognizer()
    audio_data.seek(0)  # Ensure the BytesIO object is at the beginning
    with sr.AudioFile(audio_data) as source:
        audio_text = recognizer.recognize_google(source, language='en-US')
    return audio_text



# Command to handle /stt
@app.on_message(filters.command("stt"))
async def speech_to_text(bot, message):
    if message.reply_to_message and message.reply_to_message.audio:
        audio = message.reply_to_message.audio
        audio_data = await bot.download_media(audio)
        
        # Convert audio to MP3 format
        sound = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
        mp3_data = io.BytesIO()
        sound.export(mp3_data, format="mp3")
        mp3_data.seek(0)
        
        # Convert audio to text
        text = audio_to_text(mp3_data)
        
        # Send the text as a reply
        await message.reply_text(text)
    else:
        await message.reply_text("Please reply to an audio file to convert it to text.")
