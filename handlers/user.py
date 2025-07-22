from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# ---------- СТАРТ ----------
@router.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить анкету 👩", callback_data="add_profile")],
        [InlineKeyboardButton(text="Правила ℹ️", callback_data="rules")]
    ])
    await message.answer(
        "Привет! Это бот знакомств для Ишимбая и соседних городов (Салават, Стерлитамак и другие) 💌",
        reply_markup=keyboard
    )

# ---------- СОСТОЯНИЯ ----------
class ProfileStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()

# ---------- ХЭНДЛЕР НА КНОПКУ "Добавить анкету" ----------
@router.callback_query(F.data == "add_profile")
async def add_profile_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Как тебя зовут?")
    await state.set_state(ProfileStates.name)

# ---------- ИМЯ ----------
@router.message(ProfileStates.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(ProfileStates.age)

# ---------- ВОЗРАСТ ----------
@router.message(ProfileStates.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введи возраст цифрами.")
        return
    await state.update_data(age=int(message.text))

    gender_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Парень")],
        [KeyboardButton(text="Девушка")]
    ], resize_keyboard=True)

    await message.answer("Ты парень или девушка?", reply_markup=gender_kb)
    await state.set_state(ProfileStates.gender)

# ---------- ПОЛ ----------
@router.message(ProfileStates.gender)
async def get_gender(message: Message, state: FSMContext):
    if message.text not in ["Парень", "Девушка"]:
        await message.answer("Пожалуйста, выбери из предложенных вариантов.")
        return
    await state.update_data(gender=message.text)
    await message.answer("Пришли своё фото 🖼", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProfileStates.photo)

# ---------- ФОТО ----------
@router.message(ProfileStates.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)

    data = await state.get_data()
    caption = (
        f"Анкета готова:\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n"
        f"Пол: {data['gender']}"
    )

    await message.answer_photo(photo=photo_id, caption=caption)
    await state.clear()


# Регистрируем роутер для подключения в main.py
def register_user_handlers(dp):
    dp.include_router(router)
