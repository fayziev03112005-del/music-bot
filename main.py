import logging
import sqlite3
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "PASTE_YOUR_TOKEN_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("music.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    folder TEXT,
    name TEXT,
    file_id TEXT
)
""")

conn.commit()

# ---------------- LANG ----------------
user_lang = {}

def get_text(lang, key):
    texts = {
        "start": {
            "ru": "Привет! Я музыкальный бот 🎵",
            "en": "Hello! I am a music bot 🎵"
        },
        "choose": {
            "ru": "Выбери язык:",
            "en": "Choose language:"
        }
    }
    return texts[key][lang]

# ---------------- KEYBOARDS ----------------
lang_kb = ReplyKeyboardMarkup(resize_keyboard=True)
lang_kb.add(KeyboardButton("Русский 🇷🇺"), KeyboardButton("English 🇬🇧"))

main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("➕ Folder"), KeyboardButton("🎵 My music"))

# ---------------- START ----------------
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Choose language / Выбери язык:", reply_markup=lang_kb)

# ---------------- LANGUAGE ----------------
@dp.message_handler(lambda m: m.text in ["Русский 🇷🇺", "English 🇬🇧"])
async def set_lang(message: types.Message):
    if message.text == "Русский 🇷🇺":
        user_lang[message.from_user.id] = "ru"
        await message.answer("Выбран русский язык", reply_markup=main_kb)
    else:
        user_lang[message.from_user.id] = "en"
        await message.answer("English selected", reply_markup=main_kb)

# ---------------- CREATE FOLDER ----------------
@dp.message_handler(lambda m: m.text == "➕ Folder")
async def create_folder(message: types.Message):
    lang = user_lang.get(message.from_user.id, "ru")
    await message.answer("Напиши имя папки:" if lang=="ru" else "Send folder name:")

    @dp.message_handler()
    async def save_folder(msg: types.Message):
        cur.execute("INSERT INTO folders (user_id, name) VALUES (?,?)",
                    (msg.from_user.id, msg.text))
        conn.commit()
        await msg.answer("Папка создана ✔" if lang=="ru" else "Folder created ✔")

# ---------------- RUN ----------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
