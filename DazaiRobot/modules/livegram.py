from pyrogram import Client, filters
from pyrogram.types import Message

from DazaiRobot import OWNER_ID
from DazaiRobot import pbot as bot


@bot.on_message(filters.private & filters.incoming)
async def on_pm_s(client: Client, message: Message):
    if message.from_user.id != 6265459491:
        fwded_mesg = await message.forward(chat_id=OWNER_ID, disable_notification=True)
