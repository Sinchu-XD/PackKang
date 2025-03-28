import os
import asyncio
from dotenv import load_dotenv
from pyrofork import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName, InputDocument
from pyrogram.raw.functions.stickers import CreateStickerSet, AddStickerToSet
from pyrogram.raw.types import DocumentAttributeSticker, InputMediaUploadedDocument
from pyrogram.types import Message

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID", 25024171))
API_HASH = os.getenv("API_HASH", "7e709c0f5a2b8ed7d5f90a48219cffd3")
SESSION_NAME = os.getenv("SESSION_NAME", "BQBuoD8AtOwxLV-QRgi1IWpNidBHfwrIGV_5Imu1W5c_gOrWNumbb_zoZpp3NDSadfXkdFUk_bIc_UGDGnj4vTXt3VtLpWW9_lnmdjarZ4UuR9IkomRyM-FkdCoCTbUBzw_6a4j1z_fjGiWxW98WZ6CF1EVy3AfHFRBqrcn6-z4B2R-FhgPeew_CYk8vmXEpjYu4JK9EEGF8k-abTqI0GuGJ5W6pWNqa7QmB6rWPODMDkH21_DAgo8tsTVQId01dGrWso24MihswteFdRAzhA4Xho1_OXxN7amFL0WYsXEqRFh5tpIhW4jZ8KIMteqgfkgDsRRYjYCppGIs5tW7xwrS9AnzPewAAAAHjq--iAA")

# Add SUDO users (comma-separated user IDs)
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", 7862043458).split(",")))

# Initialize Userbot Client (MUST use a Userbot, NOT a Bot Token)
app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("kangpack") & filters.reply)
async def kang_sticker_pack(client: Client, message: Message):
    """Clone a sticker pack using a Userbot (SUDO only)"""

    # Check if user is a SUDO user
    if message.from_user.id not in SUDO_USERS:
        return await message.reply_text("🚫 You are not authorized to use this command.")

    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("⚠️ Reply to a sticker to clone!")

    sticker = message.reply_to_message.sticker
    sticker_set_name = sticker.set_name

    if not sticker_set_name:
        return await message.reply_text("⚠️ This sticker is not part of any pack.")

    try:
        # Fetch sticker pack info
        sticker_set = await client.invoke(
            GetStickerSet(
                stickerset=InputStickerSetShortName(short_name=sticker_set_name),
                hash=0
            )
        )

        if not hasattr(sticker_set, "documents") or not sticker_set.documents:
            return await message.reply_text("❌ No stickers found to clone!")

        # Get user details
        user = await client.get_me()
        user_peer = await client.resolve_peer(user.id)

        # Create a new sticker pack name
        new_pack_name = f"kang_{user.id}_pack"
        new_pack_title = f"Kanged Pack by {user.first_name}"

        # Upload first sticker to create the pack
        first_sticker = sticker_set.documents[0]
        file_path = await client.download_media(first_sticker)
        uploaded = await client.invoke(
            InputMediaUploadedDocument(
                file=file_path,
                attributes=[DocumentAttributeSticker(emojis="🔥")]
            )
        )

        # Create new sticker pack
        await client.invoke(
            CreateStickerSet(
                user_id=user_peer,
                title=new_pack_title,
                short_name=new_pack_name,
                stickers=[],
                animated=False,
                masks=False
            )
        )

        # Add all stickers to the pack
        for sticker in sticker_set.documents:
            file_path = await client.download_media(sticker)
            uploaded = await client.invoke(
                InputMediaUploadedDocument(
                    file=file_path,
                    attributes=[DocumentAttributeSticker(emojis="🔥")]
                )
            )

            await client.invoke(
                AddStickerToSet(
                    user_id=user_peer,
                    stickerset=InputStickerSetShortName(short_name=new_pack_name),
                    sticker=InputDocument(
                        id=uploaded.id,
                        access_hash=uploaded.access_hash,
                        file_reference=uploaded.file_reference
                    )
                )
            )

        await message.reply_text(f"✅ Sticker pack cloned successfully!\n[View Pack](https://t.me/addstickers/{new_pack_name})")

    except Exception as e:
        await message.reply_text(f"❌ Failed to kang sticker: {str(e)}")

print("✅ Userbot is running...")
app.run()
      
