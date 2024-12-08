import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from cfg.base import cfg
from src.handler import route

dp = Dispatcher()
storage = MemoryStorage()


async def main() -> None:
    bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML), storage=storage)

    dp.include_router(route)
    await dp.start_polling(bot)


def start_asyncio_loop():
    asyncio.run(main())


if __name__ == "__main__":
    start_asyncio_loop()
