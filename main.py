import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from aiohttp import web

from handlers import user, admin  # Подключаем роутеры из handlers

# Загружаем переменные окружения из .env файла
load_dotenv()

# Проверяем, что переменные окружения загружены правильно
print(f"BOT_TOKEN: {os.getenv('BOT_TOKEN')}")
print(f"ADMIN_ID: {os.getenv('ADMIN_ID')}")
print(f"PAYMENT_PROVIDER_TOKEN: {os.getenv('PAYMENT_PROVIDER_TOKEN')}")
print(f"PRICE_RUB: {os.getenv('PRICE_RUB')}")
print(f"WEBHOOK_URL: {os.getenv('WEBHOOK_URL')}")

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

async def on_start(request):
    return web.Response(text="Bot is running!")

async def main():
    dp.include_router(user.router)  # Включаем роутер из user.py
    dp.include_router(admin.router)  # Включаем роутер из admin.py (если есть)
    
    # Настройка webhook
    app = web.Application()
    app.add_routes([web.post(f"/{TOKEN}", dp.start_webhook)])
    
    # Запуск webhook сервера
    await web.run_app(app, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    asyncio.run(main())
