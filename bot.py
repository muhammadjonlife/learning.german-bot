import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import BOT_TOKEN
from database import init_db, add_user, update_stats, update_streak, get_stats
from ai import ai_learn, ai_quiz, ai_check, ai_chat


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# STATES
class UserState(StatesGroup):
    lang = State()
    menu = State()
    quiz = State()


# KEYBOARDS
lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇹🇯 Тоҷикӣ")],
        [KeyboardButton(text="🇷🇺 Русский")],
        [KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Learn")],
        [KeyboardButton(text="📝 Quiz")],
        [KeyboardButton(text="📊 Stats")]
    ],
    resize_keyboard=True
)


LANG_MAP = {
    "🇹🇯 Тоҷикӣ": "tj",
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en"
}


# START
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    add_user(message.from_user.id)
    await message.answer("🌍 Забон интихоб кун", reply_markup=lang_kb)
    await state.set_state(UserState.lang)


# LANGUAGE
@dp.message(UserState.lang)
async def set_lang(message: Message, state: FSMContext):
    if message.text not in LANG_MAP:
        await message.answer("❌ Аз кнопка интихоб кун")
        return

    await state.update_data(lang=LANG_MAP[message.text])
    update_streak(message.from_user.id)

    await message.answer("✅ Забон интихоб шуд", reply_markup=menu_kb)
    await state.set_state(UserState.menu)


# LEARN
@dp.message(F.text == "📚 Learn")
async def learn(message: Message, state: FSMContext):
    data = await state.get_data()
    text = ai_learn(data["lang"])
    await message.answer(text)


# QUIZ
@dp.message(F.text == "📝 Quiz")
async def quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    q = ai_quiz(data["lang"])

    await state.update_data(correct=q["answer"])
    await message.answer(q["question"])
    await state.set_state(UserState.quiz)


# CHECK ANSWER
@dp.message(UserState.quiz)
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()

    correct = data.get("correct")
    ok, text = ai_check(message.text, correct)

    update_stats(message.from_user.id, ok)

    await message.answer(text)
    await state.set_state(UserState.menu)


# STATS
@dp.message(F.text == "📊 Stats")
async def stats(message: Message):
    stats = get_stats(message.from_user.id)

    if stats:
        correct, total, streak = stats
        await message.answer(
            f"📊 Статистика:\n"
            f"✔️ Дуруст: {correct}\n"
            f"📚 Ҳама: {total}\n"
            f"🔥 Стрик: {streak}"
        )
    else:
        await message.answer("Маълумот нест")


# RUN
async def main():
    init_db()
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())