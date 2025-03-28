import os
import asyncio
from pyrogram import Client, filters, types
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatJoinRequest, Message, InputMediaPhoto
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName, InputDocument
from pyrogram.raw.functions.stickers import CreateStickerSet, AddStickerToSet
from pyrogram.raw.types import DocumentAttributeSticker, InputMediaUploadedDocument
from pyrogram.types import Message


# Bot Credentials
API_ID = 25024171  # Replace with your API ID
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"  # Replace with your API HASH
BOT_TOKEN = "7043644719:AAFtq9vIrC9yRuY3Ge7Om8lYoEAGGadwR7Y"  # Replace with your BOT TOKEN

# Initialize Bot
app = Client("approve_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("approveall") & filters.group)
async def approve_requests(client, message):
    """ Approves all pending join requests in a group or channel """
    chat_id = message.chat.id

    try:
        approved_count = 0

        async for req in client.get_chat_join_requests(chat_id):  # ✅ FIXED
            await client.approve_chat_join_request(chat_id, req.user.id)
            approved_count += 1
            await asyncio.sleep(1)  # Prevents floodwait

        if approved_count == 0:
            await message.reply_text("✅ No pending join requests found!")
        else:
            await message.reply_text(f"✅ Approved {approved_count} join requests!")

    except ChatAdminRequired:
        await message.reply_text("❌ I need admin rights to approve join requests!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

print("✅ Bot is running...")





@app.on_message(filters.command("approve") & filters.reply)
async def approve_single_request(client: Client, message: Message):
    """Approve a specific user's join request by replying to their request message."""
    
    chat_id = message.chat.id

    # ✅ Ensure the user is an admin
    user_status = await client.get_chat_member(chat_id, message.from_user.id)
    if not user_status.privileges or not user_status.privileges.can_invite_users:
        return await message.reply_text("❌ You must be an **Admin** with 'Add Users' permission!")

    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply_text("❌ Reply to the user's join request message!")

    user_id = message.reply_to_message.from_user.id

    try:
        await client.approve_chat_join_request(chat_id, user_id)
        await message.reply_text(f"✅ Approved user: [{user_id}](tg://user?id={user_id})")
    except Exception as e:
        await message.reply_text(f"❌ Failed to approve user: {e}")


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
async def kang_sticker_pack(client: Client, message: Message):
    """Clone a sticker pack using a Userbot"""

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




@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handles the /start command."""
    await message.reply_text("Welcome to the Sticker Kanger Bot! Use /kang to kang a sticker, /kangpack to kang a whole pack!")


print("Mar Ja Bc")
app.run()
