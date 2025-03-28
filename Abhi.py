import os
from typing import List
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.types import Message, InputMediaDocument

# 🔹 Telegram API Credentials (Get from my.telegram.org)
API_ID = 25024171  
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7043644719:AAFtq9vIrC9yRuY3Ge7Om8lYoEAGGadwR7Y"

app = Client("sticker_kang_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("kangpack") & filters.reply)
async def kang_sticker_pack(client: Client, message: Message):
    """Clone an entire sticker pack using Pyrofork."""

    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("❌ Reply to a sticker to clone the entire pack.")

    sticker = message.reply_to_message.sticker
    sticker_set_name = sticker.set_name

    if not sticker_set_name:
        return await message.reply_text("❌ This sticker is not from a pack.")

    try:
        # ✅ Correct Pyrofork API Call (Add `hash=0`)
        sticker_set = await client.invoke(GetStickerSet(stickerset=InputStickerSetShortName(short_name=sticker_set_name), hash=0))
    except Exception as e:
        return await message.reply_text(f"❌ Error fetching sticker pack: `{str(e)}`")

    user = await client.get_me()
    new_pack_name = f"kang_{user.id}_pack"
    new_pack_title = f"Kanged Pack by {user.first_name}"

    sticker_files = []  # Store sticker file paths for cleanup
    input_stickers = []

    await message.reply_text(f"⚡ Cloning **{sticker_set.set.title}** ({len(sticker_set.packs)} stickers)...")

    for sticker in sticker_set.documents:
        sticker_file = await client.download_media(sticker)
        if sticker_file:
            input_stickers.append(InputMediaDocument(sticker_file))  # ✅ Pyrofork-Compatible
            sticker_files.append(sticker_file)

    try:
        # Check if the user already has a sticker pack
        try:
            existing_pack = await client.get_sticker_set(new_pack_name)
            await client.add_sticker_to_set(user.id, new_pack_name, stickers=input_stickers)
            msg = f"✅ Stickers added to existing pack! [View Pack](https://t.me/addstickers/{new_pack_name})"
        except:
            await client.create_sticker_set(user.id, new_pack_name, new_pack_title, stickers=input_stickers)
            msg = f"✅ New sticker pack created! [View Pack](https://t.me/addstickers/{new_pack_name})"

        await message.reply_text(msg)

    except Exception as e:
        await message.reply_text(f"❌ Failed to create sticker pack: `{str(e)}`")

    # Clean up downloaded sticker files
    for file_path in sticker_files:
        os.remove(file_path)

print("✅ Bot is running...")
app.run()
