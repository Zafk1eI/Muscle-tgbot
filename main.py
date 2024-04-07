import asyncio
import logging
from datetime import datetime
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config_reader import settings
from handlers import apsched, handler
from middlewares.middlewares import UserMiddleware


async def on_startup() -> None:
    await Tortoise.init(
        db_url=settings.DB_URL.get_secret_value(),
        modules={"models": ["db.models"]}
    )
    await Tortoise.generate_schemas()
    print("Бот и база данных запущены")


async def on_shutdown() -> None:
    await Tortoise.close_connections()
    print("Соединение закрыто")


async def main() -> None:
    bot = Bot(
        settings.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(func=apsched.every_day, trigger="cron",
                      hour=datetime.now().hour,
                      minute=datetime.now().minute + 1,
                      start_date=datetime.now(),
                      kwargs={"bot": bot})
    scheduler.start()
    dp.include_routers(
        handler.router,
        apsched.apscheduler_router
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.message.middleware(UserMiddleware())
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
