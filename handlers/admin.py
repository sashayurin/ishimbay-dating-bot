from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db import get_pending_profiles, approve_profile, reject_profile
import os

router = Router()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

@router.message(Command("approve"))
async def list_profiles(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return await message.answer("❌ Нет доступа")
    profiles = get_pending_profiles()
    if not profiles:
        return await message.answer("Нет анкет на одобрение.")
    for profile in profiles:
        uid, name, age, gender, status, code, photo = profile
        status_text = {
            "pending_payment": "❌ Ожидает оплату",
            "pending_video": f"📹 Ждёт видео (код: {code})"
        }.get(status, "Неизвестно")
        await message.answer_photo(
            photo=photo,
            caption=f"{name}, {age}, {gender}\nСтатус: {status_text}\n\n/ok_{uid} ✅ | /ban_{uid} ❌"
        )

@router.message(F.text.startswith("/ok_"))
async def ok_user(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return
    user_id = int(message.text.split("_")[1])
    approve_profile(user_id)
    await message.answer("✅ Анкета одобрена.")

@router.message(F.text.startswith("/ban_"))
async def ban_user(message: Message):
    if message.from_user.username != ADMIN_USERNAME:
        return
    user_id = int(message.text.split("_")[1])
    reject_profile(user_id)
    await message.answer("🚫 Анкета удалена.")
