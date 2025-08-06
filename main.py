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

# Обработчик для корня, чтобы проверить, что сервер работает
async def on_start(request):
    return web.Response(text="Bot is running!")

async def on_webhook(request):
    json_data = await request.json()
    update = await bot.parse_update(json_data)
    await dp.process_update(update)
    return web.Response(status=200)

async def main():
    dp.include_router(user.router)  # Включаем роутер из user.py
    dp.include_router(admin.router)  # Включаем роутер из admin.py (если есть)

    # Настройка webhook
    app = web.Application()
    
    # Настроим webhook на URL, предоставленный Render
    await bot.set_webhook(WEBHOOK_URL)  # Настройка webhook для получения запросов от Telegram
    
    # Устанавливаем роуты для приема webhook-запросов
    app.add_routes([web.post(f"/{TOKEN}", on_webhook)])

    # Запуск веб-приложения через aiohttp
    return app

# Для Render (и других систем), которые уже управляют event loop
if __name__ == "__main__":
    app = asyncio.run(main())  # Используем asyncio для подготовки и получения app
    web.run_app(app, host="0.0.0.0", port=3000)
