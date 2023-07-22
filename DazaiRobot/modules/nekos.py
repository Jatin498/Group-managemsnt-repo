import nekos  # put nekos.py in your requirements.txt
import requests
from pyrogram import filters
from pyrogram.types import CallbackQuery

from DazaiRobot import app
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from DazaiRobot import DB_URI

mongo = MongoClient(DB_URI)
dbname = mongo.NekoDb

url_sfw = "https://api.waifu.pics/sfw/"

nekomodedb = dbname.nekomode


async def is_nekomode_on(chat_id: int) -> bool:
    chat = await nekomodedb.find_one({"chat_id_toggle": chat_id})
    return not bool(chat)


async def nekomode_on(chat_id: int) -> bool:
    await nekomodedb.delete_one(
        {"chat_id_toggle": chat_id}
    )


async def nekomode_off(chat_id: int):
    await nekomodedb.insert_one(
        {"chat_id_toggle": chat_id}
    )


@app.on_message(filters.command("wallpaper"))
async def wallpaper(client, message):
    chat_id = message.chat.id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        target = "wallpaper"
        img_url = nekos.img(
            target
        )  # Replace nekos.img(target) with the correct function call
        await message.reply_photo(photo=img_url)


@app.on_message(filters.command("nekomode on"))
async def enable_nekomode(client, message):
    chat_id = message.chat.id
    await nekomode_on(chat_id)
    await message.reply("Nekomode has been enabled.")


@app.on_message(filters.command("nekomode off"))
async def disable_nekomode(client, message):
    chat_id = message.chat.id
    await nekomode_off(chat_id)
    await message.reply("Nekomode has been disabled.")


@app.on_message(
    filters.command(
        [
            "waifu",
            "neko",
            "shinobu",
            "megumin",
            "bully",
            "cuddle",
            "cry",
            "hug",
            "awoo",
            "kiss",
            "lick",
            "pat",
            "smug",
            "bonk",
            "yeet",
            "blush",
            "smile",
            "wave",
            "highfive",
            "handhold",
            "nom",
            "bite",
            "glomp",
            "slap",
            "hGojoy",
            "wink",
            "poke",
            "dance",
            "cringe",
            "tickle",
        ]
    )
)
async def nekomode_commands(client, message):
    chat_id = message.chat.id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        target = message.command[0].lower()
        url = f"{url_sfw}{target}"
        result = requests.get(url).json()
        img = result["url"]
        await message.reply_animation(img)
