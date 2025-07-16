import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
import os

BOT_TOKEN = os.getenv("MY_BOT_TOKEN")  # Установим в Render как переменную окружения

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())