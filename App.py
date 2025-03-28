import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatJoinRequest, Message


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
        async for req in client.get_chat_members(chat_id, filter="request"):
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


print("✅ Bot is running...")
app.run()
