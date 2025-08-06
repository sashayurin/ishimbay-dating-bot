import os  # Добавь этот импорт

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Получаем ADMIN_ID из переменных окружения
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Словарь для хранения заявок на проверку
pending_applications = {}

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет доступа к панели администратора.")
        return
    
    # Логика для отображения всех заявок на проверку
    if not pending_applications:
        await message.answer("📝 Нет новых заявок.")
        return

    applications = "\n".join([f"📋 {user_id} - {data['name']} ({data['gender']}, {data['age']} лет)" for user_id, data in pending_applications.items()])
    await message.answer(f"📝 Заявки на подтверждение:\n{applications}")

@router.message(Command("approve"))
async def approve_application(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет доступа к панели администратора.")
        return

    # Проверка, передан ли id пользователя для подтверждения
    if message.text.startswith("/approve"):
        user_id = message.text.split()[1] if len(message.text.split()) > 1 else None

        if user_id and int(user_id) in pending_applications:
            # Успешное подтверждение
            application = pending_applications.pop(int(user_id))
            await message.answer(f"✅ Заявка от {application['name']} подтверждена!")
            # Отправляем сообщение девушке, что её заявка подтверждена
            await message.bot.send_message(int(user_id), "Поздравляем, ваша анкета подтверждена и опубликована!")
        else:
            await message.answer("❌ Заявка не найдена или ID указан неверно.")

@router.message(Command("reject"))
async def reject_application(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ У вас нет доступа к панели администратора.")
        return

    # Проверка, передан ли id пользователя для отклонения
    if message.text.startswith("/reject"):
        user_id = message.text.split()[1] if len(message.text.split()) > 1 else None

        if user_id and int(user_id) in pending_applications:
            # Отклонение заявки
            application = pending_applications.pop(int(user_id))
            await message.answer(f"❌ Заявка от {application['name']} отклонена!")
            # Отправляем сообщение девушке, что её заявка отклонена
            await message.bot.send_message(int(user_id), "Извините, ваша анкета не прошла проверку.")
        else:
            await message.answer("❌ Заявка не найдена или ID указан неверно.")
