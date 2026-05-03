import random

WORDS = [
    {"de": "Haus", "tj": "хона"},
    {"de": "Auto", "tj": "мошин"},
    {"de": "Buch", "tj": "китоб"},
    {"de": "Wasser", "tj": "об"},
]

def ai_learn(lang):
    word = random.choice(WORDS)
    return f"📚 {word['de']} = {word['tj']}"

def ai_quiz(lang):
    word = random.choice(WORDS)
    return {
        "question": f"❓ {word['de']} = ?",
        "answer": word["tj"]
    }

def ai_check(user_answer, correct):
    if user_answer.lower() == correct.lower():
        return True, "✅ Дуруст!"
    return False, f"❌ Хато\nҶавоб: {correct}"

def ai_chat(text, lang):
    return "🤖 AI ҳоло хомӯш аст"