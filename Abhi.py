import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InputSticker, StickerSet

API_ID = 25024171  # Get from my.telegram.org
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7043644719:AAFtq9vIrC9yRuY3Ge7Om8lYoEAGGadwR7Y"


app = Client("sticker_kang_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("kangpack") & filters.reply)
async def kang_sticker_pack(client: Client, message: Message):
    if not message.reply_to_message.sticker:
        return await message.reply_text("Please reply to a sticker from the pack you want to clone.")
    
    sticker = message.reply_to_message.sticker
    sticker_set_name = sticker.set_name
    
    if not sticker_set_name:
        return await message.reply_text("This sticker is not from a pack.")
    
    try:
        sticker_set = await client.get_sticker_set(sticker_set_name)
    except Exception as e:
        return await message.reply_text(f"Error fetching sticker pack: {str(e)}")
    
    user = await client.get_me()
    new_pack_name = f"kang_{user.id}_pack"
    new_pack_title = f"Kanged Pack by {user.first_name}"
    
    stickers = []
    for sticker in sticker_set.stickers:
        sticker_file = await client.download_media(sticker)
        stickers.append(InputSticker(sticker=sticker_file, emojis=sticker.emoji or "✨"))
    
    try:
        await client.create_new_sticker_set(user.id, new_pack_name, new_pack_title, stickers=stickers)
        await message.reply_text(f"Sticker pack successfully cloned! [View Pack](https://t.me/addstickers/{new_pack_name})")
    except Exception as e:
        await message.reply_text(f"Failed to create sticker pack: {str(e)}")
    
    for sticker in stickers:
        os.remove(sticker.sticker)  # Clean up downloaded files

print("Bot is running...")
app.run()
  
