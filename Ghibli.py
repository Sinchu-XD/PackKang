import os
import requests
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot API credentials
API_ID = 25024171
API_HASH = "7952918661:AAEuNYscduy2e_WeGkhgKFSRdnQ1smqL1HE"

# Replicate API Key (Get from https://replicate.com/)
REPLICATE_API_KEY = "your_replicate_api_key"

# Initialize Bot
bot = Client("AnimeGhibliBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Convert Image to Anime Style
async def convert_to_anime(image_url: str):
    try:
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {REPLICATE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "version": "your_model_version",  # Get from Replicate AI model
                "input": {"image": image_url},
            },
        )
        result = response.json()
        return result.get("output") if result else None
    except Exception as e:
        return None

# Handle /start command
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🎨 Send me an image, and I'll turn it into Anime or Ghibli style!")

# Handle image messages
@bot.on_message(filters.photo)
async def process_image(client, message: Message):
    msg = await message.reply_text("⏳ Processing image...")

    # Download the image
    image_path = await message.download()
    image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{image_path}"

    # Convert to Anime
    anime_url = await convert_to_anime(image_url)
    if anime_url:
        await message.reply_photo(anime_url, caption="🌸 Here is your **Anime-style** image!")
    else:
        await message.reply_text("❌ Failed to convert image.")

    await msg.delete()

# Run Bot
print("🤖 Bot is running...")
bot.run()
