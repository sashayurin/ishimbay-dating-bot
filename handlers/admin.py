from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import os

router = Router()

# Получаем имя администратора из переменной окружения
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

@router.message(Command("approve"))
async def approve_profile(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        await message.answer("❌ У вас нет прав на выполнение этой команды.")
        return
    await message.answer("✅ Профиль одобрен (заглушка).")

# Эта функция обязательно нужна для подключения роутера в main.py
def register_admin_handlers(dp):
    dp.include_router(router)
