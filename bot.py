import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from ai import fix_error, just_ai
from audio import transcript_audio
from questions import qm

token = '7808767389:AAHojjVNOsFnpFzHismcrrKcrg7zIxeymrc'
bot = Bot(token=token)
dp = Dispatcher()


class NEW(StatesGroup):
    one = State()

@dp.message(CommandStart())
async def echo(message: Message,state:FSMContext):
    await message.reply("Hello, world!\nThis is test mode so it maybe works slowly depending on your speech length")
    await state.clear()

async def send_long_reply(message, text):
        if text is None:
            await message.answer("⚠️ AI failed to generate a response. Please try again.")
            return
        chunks = [text[i:i + 4090] for i in range(0, len(text), 4090)]
        print(chunks)
        for chunk in chunks:
            await message.answer(text=chunk, parse_mode='HTML')

# Usage:

@dp.message(F.text == "question")
async def question(message: Message,state: FSMContext):
    qm.cleanup()  # Delete previous audio if exists
    question_text, audio_path = qm.get_next_question()

    if not question_text:
        await message.answer("✅ All questions completed!")
        return

    audio = FSInputFile(audio_path)
    await message.answer_audio(audio, caption=question_text)
    await state.set_state(NEW.one)

@dp.message(NEW.one)
async def new_audio_somthing(message: Message, state: FSMContext):
    if not message.audio:
        await message.answer(text='Please send a voice message')
        return
    await message.reply(text='Your speech is scoring please wait')
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path
    destination = f"{voice.file_unique_id}.ogg"
    await bot.download_file(file_path, destination)
    text = transcript_audio(destination)
    await send_long_reply(message, text)


@dp.message(F.voice)
async def voice(message: Message):
    voice = message.voice
    file = await bot.get_file(voice.file_id)
    file_path = file.file_path
    destination = f"{voice.file_unique_id}.ogg"
    await message.reply(text='Scoring you speech')
    await bot.download_file(file_path, destination)
    text = transcript_audio(destination)
    await send_long_reply(message,text)



@dp.message(F.document)
async def document(message: Message):
    await message.answer(text=f"id:{message.document.file_id}")



@dp.message(F.text.startswith('.'))
async def default(message: Message):
    text = message.text[1:]
    await message.answer(text=just_ai(text),parse_mode='HTML')

if __name__ == '__main__':
    try:
        asyncio.run(dp.start_polling(bot, skip_updates=True))
    except KeyboardInterrupt:
        pass