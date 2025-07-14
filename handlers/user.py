
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавить анкету 👩", callback_data="add_profile")],
        [InlineKeyboardButton(text="Правила ℹ️", callback_data="rules")]
    ])
    await message.answer("Привет! Это бот знакомств для Ишимбая 💌", reply_markup=keyboard)

def register_user_handlers(dp):
    dp.include_router(router)
