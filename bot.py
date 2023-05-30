import asyncio
import logging
from aiogram import Bot, Dispatcher
import heandlers

# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    # получаем токен и создаем объект бота
    with open("token.txt", "r") as token:
        api_token: str = token.read()
    bot = Bot(token=api_token)

    # Диспетчер
    dp = Dispatcher()
    dp.include_router(heandlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())