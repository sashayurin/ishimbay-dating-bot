import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from aiohttp import web

from handlers import user, admin  # Подключаем роутеры из handlers

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик для корня
async def on_start(request):
    return web.Response(text="Bot is running!")

async def main():
    dp.include_router(user.router)  # Включаем роутер из user.py
    dp.include_router(admin.router)  # Включаем роутер из admin.py (если есть)
    
    # Настройка webhook
    app = web.Application()
    app.add_routes([web.post(f"/{TOKEN}", dp.handle_webhook)])

    # Запуск веб-сервера через aiohttp
    await web.run_app(app, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    asyncio.run(main())
