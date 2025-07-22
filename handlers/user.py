from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiosqlite

router = Router()

class ProfileStates(StatesGroup):
    name = State()
    age = State()
    gender = State()
    photo = State()

@router.message(CommandStart())
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить анкету 👩", callback_data="add_profile")],
        [InlineKeyboardButton(text="Правила ℹ️", callback_data="rules")]
    ])
    await message.answer("Привет! Это бот знакомств 💌", reply_markup=kb)

@router.callback_query(F.data == "add_profile")
async def add_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Как тебя зовут?")
    await state.set_state(ProfileStates.name)

@router.message(ProfileStates.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(ProfileStates.age)

@router.message(ProfileStates.age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Возраст должен быть числом.")
    await state.update_data(age=int(message.text))
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Парень")],
        [KeyboardButton(text="Девушка")]
    ], resize_keyboard=True)
    await message.answer("Ты парень или девушка?", reply_markup=kb)
    await state.set_state(ProfileStates.gender)

@router.message(ProfileStates.gender)
async def get_gender(message: Message, state: FSMContext):
    if message.text not in ["Парень", "Девушка"]:
        return await message.answer("Выбери из кнопок.")
    await state.update_data(gender=message.text)
    await message.answer("Пришли своё фото 🖼", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ProfileStates.photo)

@router.message(ProfileStates.photo, F.photo)
async def get_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id

    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT INTO profiles (user_id, name, age, gender, photo) VALUES (?, ?, ?, ?, ?)",
            (message.from_user.id, data["name"], data["age"], data["gender"], photo_id)
        )
        await db.commit()

    caption = (
        f"Твоя анкета:\n\n"
        f"<b>Имя:</b> {data['name']}\n"
        f"<b>Возраст:</b> {data['age']}\n"
        f"<b>Пол:</b> {data['gender']}\n\n"
        f"Ожидает одобрения администратором ✅"
    )
    await message.answer_photo(photo_id, caption=caption)
    await state.clear()
