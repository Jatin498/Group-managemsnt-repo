import html
import json
import re
from time import sleep

import requests
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import DazaiRobot.modules.sql.chatbot_sql as sql
from DazaiRobot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from DazaiRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from DazaiRobot.modules.log_channel import gloggable


@user_admin_no_reply
@gloggable
def dazairm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_dazai = sql.set_dazai(chat.id)
        if is_dazai:
            is_dazai = sql.set_dazai(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_DISABLED\n"
                f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin_no_reply
@gloggable
def dazaiadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_dazai = sql.rem_dazai(chat.id)
        if is_dazai:
            is_dazai = sql.rem_dazai(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_ENABLE\n"
                f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "{} ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {}.".format(
                    dispatcher.bot.first_name, mention_html(user.id, user.first_name)
                ),
                parse_mode=ParseMode.HTML,
            )

    return ""


@user_admin
@gloggable
def dazai(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "• ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="add_chat({})"),
                InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="rm_chat({})"),
            ],
        ]
    )
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def dazai_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "dazai":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message:
        if reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_dazai = sql.is_dazai(chat_id)
    if is_dazai:
        return

    if message.text and not message.document:
        if not dazai_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        request = requests.get(
            f"https://api.safone.me/chatbot?query={message.text}&user_id={chat_id}&bot_name=Group_Controller&bot_master=Mukesh"
        )
        results = json.loads(request.text)
        sleep(0.5)
        message.reply_text(results["response"])


__help__ = f"""
*{BOT_NAME} ʜᴀs ᴀɴ ᴄʜᴀᴛʙᴏᴛ ᴡʜɪᴄʜ ᴘʀᴏᴠɪᴅᴇs ʏᴏᴜ ᴀ sᴇᴇᴍɪɴɢʟᴇss ᴄʜᴀᴛᴛɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ :**

 »  /ᴄʜᴀᴛʙᴏᴛ *:* sʜᴏᴡs ᴄʜᴀᴛʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ
"""

__mod_name__ = "ᑕᕼᗩTᗷOT"


CHATBOTK_HANDLER = CommandHandler("chatbot", dazai, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(dazaiadd, pattern=r"add_chat", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(dazairm, pattern=r"rm_chat", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]
