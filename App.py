import asyncio
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, Message

# 🔹 Get API Credentials from my.telegram.org
API_ID = 25024171  
API_HASH = "7e709c0f5a2b8ed7d5f90a48219cffd3"
BOT_TOKEN = "7043644719:AAFtq9vIrC9yRuY3Ge7Om8lYoEAGGadwR7Y"

app = Client("approve_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("approveall") & filters.chat)
async def approve_all_requests(client: Client, message: Message):
    """Approve all pending join requests in groups and channels."""

    chat_id = message.chat.id

    # ✅ Ensure the user is an admin
    user_status = await client.get_chat_member(chat_id, message.from_user.id)
    if not user_status.privileges or not user_status.privileges.can_invite_users:
        return await message.reply_text("❌ You must be an **Admin** with 'Add Users' permission!")

    approved_count = 0

    async for join_request in client.get_chat_join_requests(chat_id):
        try:
            await client.approve_chat_join_request(chat_id, join_request.from_user.id)
            approved_count += 1
            await asyncio.sleep(1)  # Prevents rate limiting
        except Exception as e:
            print(f"⚠ Failed to approve {join_request.from_user.id}: {e}")

    if approved_count == 0:
        return await message.reply_text("✅ No pending join requests!")

    await message.reply_text(f"✅ Approved **{approved_count}** join requests!")


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


print("✅ Bot is running...")
app.run()
