import asyncio

from app.bot.bot import create_bot
from app.bot.middleware import CheckUserMiddleware
from app.bot.routers.commands import commands_router
from app.bot.routers.imeicheck import imeicheck_router
from app.core.config import Settings
from app.db.connector import PostgresConnector
from app.db.crud import WhileUsersListRepository
from app.services.logger.logger import AppLogger

logger = AppLogger("main")

logger.debug("Загружаем переменные окружения.")
settings = Settings()

logger.debug("Создаем экземпляр коннектора.")
pg_connector = PostgresConnector(settings=settings)

logger.debug("Создаем список роутеров.")
routers_list = [commands_router, imeicheck_router]

logger.debug("Создаем список миддлвари.")
middlewares = [CheckUserMiddleware]


async def start_bot(token: str):
    """
    Запускает бота с указанными параметрами.

    :param token: str - токен для подключения бота.
    :return: запускает процесс polling для бота.
    """
    logger.debug("Создаем бот и диспетчер.")
    bot, dp = await create_bot(
        token=token,
        routers=routers_list,
        middlewares=middlewares,
        pg_connector=pg_connector,
        repository=WhileUsersListRepository,
        settings=settings,
    )
    await dp.start_polling(bot)


async def create_app():
    """
    Создает и запускает приложение.

    :return: Запускает асинхронную задачу для старта бота.
    """
    logger.debug("Создаем асинхронную задачу для бота.")
    bot_task = asyncio.create_task(
        start_bot(
            settings.BOT_TOKEN.get_secret_value()
        )
    )
    await bot_task


if __name__ == "__main__":
    asyncio.run(create_app())
