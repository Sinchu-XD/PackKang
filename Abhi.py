import os
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet, GetDocumentByHash
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.types import Message

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
        # ✅ Fetch sticker set details correctly
        sticker_set = await client.invoke(GetStickerSet(stickerset=InputStickerSetShortName(short_name=sticker_set_name), hash=0))

        # 🔹 Extract sticker documents
        stickers = getattr(sticker_set, "documents", [])
        if not stickers:
            return await message.reply_text("❌ No stickers found in this pack.")

    except Exception as e:
        return await message.reply_text(f"❌ Error fetching sticker pack: `{str(e)}`")

    await message.reply_text(f"⚡ Cloning **{sticker_set.set.title}** ({len(stickers)} stickers)...")

    sticker_files = []

    for sticker_doc in stickers:
        try:
            # ✅ Extract required fields for download
            file_id = sticker_doc.id
            access_hash = sticker_doc.access_hash
            file_reference = sticker_doc.file_reference

            # ✅ Fetch document using GetDocumentByHash
            document = await client.invoke(GetDocumentByHash(id=file_id, access_hash=access_hash, file_reference=file_reference))

            # ✅ Download sticker properly
            sticker_file = await client.download_media(document)
            sticker_files.append(sticker_file)

        except Exception as e:
            print(f"⚠ Failed to download sticker: {e}")
            continue

    # 🚨 **FIX: Ensure stickers exist before proceeding**
    if not sticker_files:
        return await message.reply_text("❌ No stickers found to clone!")

    await message.reply_text(f"✅ Successfully cloned {len(sticker_files)} stickers!")

    # Clean up downloaded sticker files
    for file_path in sticker_files:
        os.remove(file_path)

print("✅ Bot is running...")
app.run()
