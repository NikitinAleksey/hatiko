import os

import pydantic
import pydantic_settings

__all__ = ["Settings"]


class Settings(pydantic_settings.BaseSettings):
    """
    Настройки для проекта, загружаемые из .env файла.

    :param BOT_TOKEN: SecretStr - токен для бота Telegram.
    :param TOKEN_API_LIVE: SecretStr - токен для API LIVE.
    :param POSTGRES_USER: Str - имя пользователя для подключения к базе данных
    PostgreSQL.
    :param POSTGRES_PASSWORD: SecretStr - пароль для подключения к базе данных
    PostgreSQL.
    :param POSTGRES_DB_NAME: Str - имя базы данных PostgreSQL.
    :param POSTGRES_HOST: Str - хост для подключения к базе данных PostgreSQL.
    :param POSTGRES_PORT: Int - порт для подключения к базе данных PostgreSQL.
    :param POOL_SIZE: Int - размер пула соединений для базы данных.
    :param MAX_OVERFLOW: Int - максимальное количество дополнительных
    соединений.
    :param DEBUG: Bool - флаг для режима отладки.
    """

    BOT_TOKEN: pydantic.SecretStr
    TOKEN_API_LIVE: pydantic.SecretStr

    IMEICHECK_URL: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: pydantic.SecretStr
    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    POOL_SIZE: int
    MAX_OVERFLOW: int

    WHITE_LIST: str

    DEBUG: bool

    class Config:
        env_file = os.path.abspath(os.path.join("..", ".env"))
