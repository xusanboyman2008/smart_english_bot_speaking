import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message

from ai import fix_error
from audio import transcript_audio

token = '7234794963:AAHHXY24n_GRw3Q65UbXzX1C3H_q48bmmoQ'
bot = Bot(token=token)
dp = Dispatcher()


@dp.message(CommandStart())
async def echo(message: Message):
    await message.reply("Hello, world!")

async def send_long_reply(message, text, parse_mode="HTML"):
        max_length = 4096
        chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
        for i, chunk in enumerate(chunks):
            if i == 0:
                await message.reply(f"Speaking feedbacks for {message.from_user.full_name}\n{chunk}", parse_mode=parse_mode)
            else:
                await message.answer(chunk, parse_mode=parse_mode)
# Usage:

@dp.message(F.voice)
async def voice(message: Message):
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path
    destination = f"{voice.file_unique_id}.ogg"
    await bot.download_file(file_path, destination)
    text = transcript_audio(destination)
    await send_long_reply(message, text)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot, skip_updates=True))