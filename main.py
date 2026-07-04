import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "PASTE_YOUR_TOKEN_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("music.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT
)
""")
conn.commit()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎵 Bot is running!")

@dp.message()
async def all_messages(message: types.Message):
    if message.text:
        cur.execute(
            "INSERT INTO folders (user_id, name) VALUES (?,?)",
            (message.from_user.id, message.text)
        )
        conn.commit()
        await message.answer(f"Saved ✔ {message.text}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
