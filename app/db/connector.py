from contextlib import asynccontextmanager
from typing import AsyncIterator

import pydantic_settings
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

__all__ = ["PostgresConnector"]


class PostgresConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Синглтон класса коннектора.

        :return: единственный экземпляр класса коннектора.
        """
        if not cls._instance:
            cls._instance = super(PostgresConnector, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings: pydantic_settings.BaseSettings):
        """
        Инициализирует параметры подключения к базе данных и создает сессии.

        :param settings: Экземпляр класса Settings с переменными окружения.
        """
        if settings and not hasattr(self, "initialized"):
            self.postgres_user = settings.POSTGRES_USER
            self.postgres_password = (settings.POSTGRES_PASSWORD.
                                      get_secret_value())
            self.postgres_db_name = settings.POSTGRES_DB_NAME
            self.postgres_host = settings.POSTGRES_HOST
            self.postgres_port = settings.POSTGRES_PORT
            self.echo = settings.DEBUG
            self.pool_size = settings.POOL_SIZE
            self.max_overflow = settings.MAX_OVERFLOW
            self.db_url = self.url_builder()
            self.engine = self.create_engine()
            self.async_session = self.create_session()
            self.initialized = True

    def url_builder(self) -> str:
        """
        Создает ссылку для подключения к базе данных.

        :return: str - строка с URL для подключения.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db_name}"
        )

    def create_engine(self) -> AsyncEngine:
        """
        Создает и возвращает движок для работы с базой данных.

        :return: AsyncEngine - движок SQLAlchemy для асинхронной работы.
        """
        return create_async_engine(
            self.db_url,
            echo=self.echo,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
        )

    def create_session(self) -> sessionmaker[AsyncSession]:
        """
        Создает пул сессий для работы с базой данных.

        :return: Фабрика сессий для асинхронной работы с базой данных.
        """
        return sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Возвращает объект сессии из пула.

        :return: AsyncSession - объект сессии для выполнения запросов.
        """
        async with self.async_session() as session:
            yield session

    def close(self) -> None:
        """
        Закрывает соединение с пулом.

        :return: None
        """
        if self.engine:
            self.engine.dispose()
