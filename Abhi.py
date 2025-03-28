import os
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet, GetDocumentByHash
from pyrogram.raw.functions.stickers import CreateStickerSet, AddStickerToSet
from pyrogram.raw.types import InputStickerSetShortName, InputStickerSetID, InputDocument, DocumentAttributeSticker
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
        # ✅ Correct Pyrofork API Call (Added `hash=0`)
        sticker_set = await client.invoke(GetStickerSet(stickerset=InputStickerSetShortName(short_name=sticker_set_name), hash=0))
    except Exception as e:
        return await message.reply_text(f"❌ Error fetching sticker pack: `{str(e)}`")

    user = await client.get_me()
    new_pack_name = f"kang_{user.id}_pack"
    new_pack_title = f"Kanged Pack by {user.first_name}"

    sticker_files = []  # Store sticker file paths for cleanup
    input_stickers = []

    await message.reply_text(f"⚡ Cloning **{sticker_set.set.title}** ({len(sticker_set.packs)} stickers)...")

    # ✅ FIX: Use `sticker_set.documents` correctly with `GetDocumentByHash`
    for sticker_doc in sticker_set.documents:
        try:
            # ✅ Use `GetDocumentByHash` instead of `GetDocumentById`
            full_doc = await client.invoke(GetDocumentByHash(sha256=sticker_doc.sha256, size=sticker_doc.size, mime_type=sticker_doc.mime_type))
            sticker_file = await client.download_media(full_doc.document)  # ✅ Proper download
        except Exception as e:
            print(f"⚠ Failed to download sticker: {e}")
            continue

        if sticker_file:
            sticker_files.append(sticker_file)

            # ✅ Prepare sticker document format for Pyrofork
            input_stickers.append(
                InputDocument(
                    id=full_doc.document.id,
                    access_hash=full_doc.document.access_hash,
                    file_reference=full_doc.document.file_reference
                )
            )

    try:
        # Check if the user already has a sticker pack
        try:
            existing_pack = await client.invoke(GetStickerSet(stickerset=InputStickerSetShortName(short_name=new_pack_name), hash=0))
            await client.invoke(
                AddStickerToSet(
                    stickerset=InputStickerSetID(id=existing_pack.set.id, access_hash=existing_pack.set.access_hash),
                    sticker=input_stickers[0],  # ✅ Pyrofork requires one sticker at a time
                    emojis="✨"
                )
            )
            msg = f"✅ Stickers added to existing pack! [View Pack](https://t.me/addstickers/{new_pack_name})"
        except:
            await client.invoke(
                CreateStickerSet(
                    user_id=user.id,
                    title=new_pack_title,
                    short_name=new_pack_name,
                    stickers=[
                        DocumentAttributeSticker(  # ✅ Required for creating stickers in Pyrofork
                            sticker=input_stickers[0],  # ✅ Pyrofork requires one sticker at a time
                            alt="✨",
                            mask=False
                        )
                    ],
                    animated=False,
                    videos=False
                )
            )
            msg = f"✅ New sticker pack created! [View Pack](https://t.me/addstickers/{new_pack_name})"

        await message.reply_text(msg)

    except Exception as e:
        await message.reply_text(f"❌ Failed to create sticker pack: `{str(e)}`")

    # Clean up downloaded sticker files
    for file_path in sticker_files:
        os.remove(file_path)

print("✅ Bot is running...")
app.run()
