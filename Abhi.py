import os
import asyncio
from pyrogram import Client, filters, types
from pyrogram.types import Message, InputMediaPhoto

# Replace with your API credentials and bot token
API_ID = 25024171  
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7043644719:AAFtq9vIrC9yRuY3Ge7Om8lYoEAGGadwR7Y"


app = Client("sticker_kang_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("kang") & filters.reply)
async def kang_sticker(client: Client, message: Message):
    """Kangs a sticker from a replied message."""
    if message.reply_to_message.sticker:
        sticker = message.reply_to_message.sticker
        sticker_file = await client.download_media(sticker.file_id)
        try:
            await client.send_sticker("me", sticker=sticker_file)
            await message.reply_text("Sticker kanged!")
        except Exception as e:
            await message.reply_text(f"Failed to kang sticker: {e}")
        finally:
            if os.path.exists(sticker_file):
                os.remove(sticker_file)

    elif message.reply_to_message.photo:
        photo = message.reply_to_message.photo
        photo_file = await client.download_media(photo.file_id)
        try:
            await client.send_sticker("me", sticker=photo_file)
            await message.reply_text("Photo kanged as sticker!")
        except Exception as e:
            await message.reply_text(f"Failed to kang photo: {e}")
        finally:
            if os.path.exists(photo_file):
                os.remove(photo_file)
    elif message.reply_to_message.animation:
        animation = message.reply_to_message.animation
        animation_file = await client.download_media(animation.file_id)
        try:
            await client.send_sticker("me", sticker=animation_file)
            await message.reply_text("GIF kanged as sticker!")
        except Exception as e:
            await message.reply_text(f"Failed to kang gif: {e}")
        finally:
            if os.path.exists(animation_file):
                os.remove(animation_file)

    else:
        await message.reply_text("Reply to a sticker, photo, or gif to kang it!")

@app.on_message(filters.command("kangpack") & filters.reply)
async def kang_pack(client: Client, message: Message):
    """Kangs an entire sticker pack from a replied message."""
    if message.reply_to_message.sticker:
        sticker_set = await client.get_sticker_set(message.reply_to_message.sticker.set_name)
        kang_count = 0
        failed_count = 0
        for sticker in sticker_set.stickers:
            sticker_file = await client.download_media(sticker.file_id)
            try:
                await client.send_sticker("me", sticker=sticker_file)
                kang_count += 1
            except Exception as e:
                failed_count += 1
                print(f"Failed to kang sticker: {e}")
            finally:
                if os.path.exists(sticker_file):
                    os.remove(sticker_file)

        await message.reply_text(f"Kanged {kang_count} stickers. Failed to kang {failed_count} stickers.")
    else:
        await message.reply_text("Reply to a sticker to kang the whole pack!")

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handles the /start command."""
    await message.reply_text("Welcome to the Sticker Kanger Bot! Use /kang to kang a sticker, /kangpack to kang a whole pack!")

async def main():
    """Main function to start the bot."""
    await app.start()
    print("Bot started. Listening for commands...")
    await asyncio.Future()  # Keep the bot running

if __name__ == "__main__":
    asyncio.run(main())
