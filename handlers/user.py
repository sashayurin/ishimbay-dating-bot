from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart

router = Router()

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

@router.callback_query(F.data == "rules")
async def rules_callback(callback: CallbackQuery):
    await callback.message.answer(
        "📌 <b>Правила использования бота:</b>\n\n"
        "1. Уважайте других участников.\n"
        "2. Не публикуйте ложную информацию.\n"
        "3. Жалобы рассматриваются администрацией.\n\n"
        "Приятного общения! 😊",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "add_profile")
async def add_profile_callback(callback: CallbackQuery):
    await callback.message.answer("📷 Давайте начнём добавление анкеты! (функция пока в разработке...)")
    await callback.answer()

def register_user_handlers(dp):
    dp.include_router(router)
