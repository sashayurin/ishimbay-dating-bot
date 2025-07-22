from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import os
import aiosqlite

router = Router()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

@router.message(Command("approve"))
async def approve_profile(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return await message.answer("❌ У вас нет прав на эту команду.")

    user_id = message.from_user.id

    async with aiosqlite.connect("users.db") as db:
        await db.execute("UPDATE profiles SET is_approved = 1 WHERE user_id = ?", (user_id,))
        await db.commit()

    await message.answer("✅ Анкета одобрена.")
