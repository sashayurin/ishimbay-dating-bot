import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from db import init_db
from handlers import register_all_handlers

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    try:
        logging.basicConfig(level=logging.INFO)
        bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()

        await init_db()  # 🔸 Инициализация базы данных

        register_all_handlers(dp)

        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка при запуске: {e}")

if __name__ == "__main__":
    asyncio.run(main())
