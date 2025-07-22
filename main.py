import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import user  # Импортируем роутер пользователя

# Вставь сюда свой токен от BotFather
TOKEN = "8088318424:AAHe8zUKX4nC2SoqcW983UmlT_SLIkOPBUY"

# Включаем логирование
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(user.router)

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
