from aiogram.fsm.state import StatesGroup, State

class UserState(StatesGroup):
    lang = State()
    mode = State()          # chat / quiz / learn
    waiting_answer = State()