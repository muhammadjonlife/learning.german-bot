from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def lang_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇹🇯 Тоҷикӣ")],
            [KeyboardButton(text="🇷🇺 Русский")],
            [KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    )

def menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💬 Chat"), KeyboardButton(text="🧠 Quiz")],
            [KeyboardButton(text="📚 Learn"), KeyboardButton(text="📊 Progress")]
        ],
        resize_keyboard=True
    )