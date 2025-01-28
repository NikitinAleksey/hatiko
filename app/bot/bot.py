from typing import List

import pydantic_settings
from aiogram import BaseMiddleware, Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connector import PostgresConnector
from app.db.crud import WhileUsersListRepository
from app.services.logger.logger import AppLogger

__all__ = ["create_bot"]

logger = AppLogger("bot")


async def register_all_routers(dp: Dispatcher, routers: List[Router]):
    """
    Регистрирует все роутеры в диспетчере.

    :param dp: Dispatcher - объект диспетчера для регистрации роутеров.
    :param routers: List[Router] - список роутеров для регистрации.
    :return: None
    """
    logger.debug("Регистрируем роутеры.")

    for router in routers:
        dp.include_router(router=router)


async def register_all_middleware(
    dp: Dispatcher,
    middlewares: List[type[BaseMiddleware]],
    session: AsyncSession,
    repository: type[WhileUsersListRepository],
    settings: pydantic_settings.BaseSettings,
):
    """
    Регистрирует все миддлварь в диспетчере.

    :param repository: CRUD для работы с бд.
    :param session: Сессия для подключения к бд.
    :param dp: Dispatcher - объект диспетчера для регистрации миддлвари.
    :param middlewares: List[BaseMiddleware] - миддлвари для регистрации.
    :param settings: pydantic_settings.BaseSettings - переменные окружения.
    :return: None
    """
    logger.debug("Регистрируем миддлвари.")

    for middleware in middlewares:
        dp.update.middleware(middleware(session, repository, settings))


async def create_bot(
    token: str,
    routers: List[Router],
    middlewares: List[type[BaseMiddleware]],
    pg_connector: PostgresConnector,
    repository: type[WhileUsersListRepository],
    settings: pydantic_settings.BaseSettings,
):
    """
    Создает экземпляры бота и диспетчера с зарегистрированными
    роутерами и миддлварами.

    :param repository: CRUD для работы с бд.
    :param pg_connector: Синглтон класса PostgresConnector для
    получения пула соединений с бд.
    :param token: str - токен для бота.
    :param routers: List[Router] - список роутеров для
    регистрации.
    :param middlewares: List[BaseMiddleware] - список миддлваров
    для регистрации.
    :param settings: pydantic_settings.BaseSettings - переменные
    окружения.
    :return: Tuple[Bot, Dispatcher] - объекты бота и диспетчера.
    """
    logger.debug("Запуск создания бота и диспетчера.")

    async with pg_connector.get_session() as session:
        bot = Bot(token=token)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        await register_all_routers(dp=dp, routers=routers)
        await register_all_middleware(
            dp=dp,
            middlewares=middlewares,
            session=session,
            repository=repository,
            settings=settings,
        )
        return bot, dp
