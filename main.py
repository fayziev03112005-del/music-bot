import asyncio
import logging
import os
import yt_dlp

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8947717361:AAGnRRbCGzFgcocrimcfq1ZOqhGULqnIf74"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def download_music(query: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "music.%(ext)s",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("🎵 Music bot ready!\nSend song name")

@dp.message()
async def music(message: Message):
    await message.answer("⏳ Downloading...")

    try:
        download_music(message.text)

        for file in os.listdir():
            if file.startswith("music"):
                await message.answer_audio(audio=open(file, "rb"))
                os.remove(file)
                break

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
