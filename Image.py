import os
import asyncio
from pyrogram import Client, filters
from real_esrgan import RealESRGAN
from PIL import Image

# ✅ Bot API Configuration (Replace with your own API credentials)
API_ID = 25024171  # Your API ID
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"  # Your API Hash
BOT_TOKEN = "7952918661:AAEuNYscduy2e_WeGkhgKFSRdnQ1smqL1HE"  # Replace with your bot token

app = Client("image_enhancer_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ Ensure output directory exists
os.makedirs("enhanced_images", exist_ok=True)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 **Welcome to Image Enhancer Bot!**\nSend me an image, and I'll enhance its quality 4x in Full HDR!")

@app.on_message(filters.photo)
async def enhance_image(client, message):
    """Enhances image quality using Real-ESRGAN (4x)"""
    
    try:
        # ✅ Download the image
        photo = message.photo
        file_path = await client.download_media(photo.file_id)

        # ✅ Load ESRGAN Model
        model = RealESRGAN("weights/realesrgan-x4.pth")
        model.load_model()

        # ✅ Enhance Image
        image = Image.open(file_path)
        enhanced_image = model.enhance(image, scale=4)  # 4x Enhancement

        # ✅ Save Enhanced Image
        enhanced_path = f"enhanced_images/enhanced_{message.from_user.id}.jpg"
        enhanced_image.save(enhanced_path)

        # ✅ Send Enhanced Image Back
        await message.reply_photo(enhanced_path, caption="✨ **Here is your enhanced 4x HDR image!**")

        # ✅ Cleanup
        os.remove(file_path)
        os.remove(enhanced_path)

    except Exception as e:
        await message.reply_text(f"❌ **Failed to enhance image:** {str(e)}")

# ✅ Start the Bot
print("🚀 Image Enhancer Bot is running...")
app.run()
