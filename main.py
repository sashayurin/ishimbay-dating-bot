import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ВАЖНО: именно BOT_TOKEN, без MY_

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
