
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import os

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

router = Router()

@router.message(Command("approve"))
async def approve_profile(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return await message.answer("У вас нет прав.")
    await message.answer("Профиль одобрен (заглушка).")

def register_admin_handlers(dp):
    dp.include_router(router)
