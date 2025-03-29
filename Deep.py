from pyrogram import Client, filters
import requests
import os

# Initialize the bot
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

bot = Client("image_converter_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to convert image using an AI API
def convert_image(image_path, style):
    url = "https://api.deepai.org/api/deepart"  # Replace with actual anime conversion API
    headers = {"api-key": "your_api_key"}
    files = {"image": open(image_path, "rb")}
    data = {"style": style}  # Example: 'ghibli' or 'anime'
    
    response = requests.post(url, files=files, headers=headers, data=data)
    result = response.json()
    return result.get("output_url")

@bot.on_message(filters.photo & filters.command(["anime", "ghibli"]))
def image_to_anime(client, message):
    style = "anime" if "anime" in message.command else "ghibli"
    photo = message.photo.file_id
    
    file_path = bot.download_media(photo)
    
    converted_url = convert_image(file_path, style)
    
    if converted_url:
        message.reply_photo(converted_url, caption=f"Here is your {style}-styled image!")
    else:
        message.reply_text("Failed to convert the image. Please try again later.")
    
    os.remove(file_path)  # Clean up the downloaded file

print("Bot is running...")
bot.run()
