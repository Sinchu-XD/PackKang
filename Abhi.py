import os
from pyrogram import Client, filters
from pyrogram.types import Message, InputSticker

# Telegram API Credentials (Get from my.telegram.org)
API_ID = 25024171  
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7043644719:AAFtq9vIrC9yRuY3Ge7Om8lYoEAGGadwR7Y"

app = Client("sticker_kang_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("kangpack") & filters.reply)
async def kang_sticker_pack(client: Client, message: Message):
    """Clone an entire sticker pack in one command."""
    
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("❌ Reply to a sticker to clone the entire pack.")
    
    sticker = message.reply_to_message.sticker
    sticker_set_name = sticker.set_name

    if not sticker_set_name:
        return await message.reply_text("❌ This sticker is not from a pack.")

    try:
        sticker_set = await client.get_sticker_set(sticker_set_name)
    except Exception as e:
        return await message.reply_text(f"❌ Error fetching sticker pack: `{str(e)}`")

    user = await client.get_me()
    new_pack_name = f"kang_{user.id}_pack"
    new_pack_title = f"Kanged Pack by {user.first_name}"

    stickers = []
    temp_files = []  # Store sticker file paths for cleanup

    await message.reply_text(f"⚡ Cloning **{sticker_set.title}** ({len(sticker_set.stickers)} stickers)...")

    for sticker in sticker_set.stickers:
        sticker_file = await client.download_media(sticker)
        if sticker_file:
            stickers.append(InputSticker(sticker=sticker_file, emojis=sticker.emoji or "✨"))
            temp_files.append(sticker_file)

    try:
        # Check if the user already has a sticker pack
        try:
            existing_pack = await client.get_sticker_set(new_pack_name)
            await client.add_sticker_to_set(user.id, new_pack_name, stickers=stickers)
            msg = f"✅ Stickers added to existing pack! [View Pack](https://t.me/addstickers/{new_pack_name})"
        except:
            await client.create_sticker_set(user.id, new_pack_name, new_pack_title, stickers=stickers)
            msg = f"✅ New sticker pack created! [View Pack](https://t.me/addstickers/{new_pack_name})"
        
        await message.reply_text(msg)
    
    except Exception as e:
        await message.reply_text(f"❌ Failed to create sticker pack: `{str(e)}`")

    # Clean up downloaded sticker files
    for file_path in temp_files:
        os.remove(file_path)

print("✅ Bot is running...")
app.run()
