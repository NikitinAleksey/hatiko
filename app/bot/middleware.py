import json
import os.path
from typing import Any, Awaitable, Callable, Dict

import aiofiles
import pydantic
import pydantic_settings
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.check.imiecheck import get_imei_info
from app.services.logger.logger import AppLogger
from app.services.validators.imei import IMEIValidator

__all__ = ["CheckUserMiddleware"]

logger = AppLogger("middleware")


class CheckUserMiddleware(BaseMiddleware):
    """
    Миддлвари для проверки наличия пользователя в разрешенных.
    """

    def __init__(
        self,
        session: AsyncSession,
        repository: "WhileUsersListRepository",
        settings: pydantic_settings.BaseSettings,
    ):
        super().__init__()
        self.session = session
        self.repository = repository
        self.imeicheck_url = settings.IMEICHECK_URL
        self.imeicheck_token = settings.TOKEN_API_LIVE

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Проверка пользователя и обработка события,
        если событие не является командой.

        :param handler: Обработчик события.
        :param event: Событие Telegram.
        :param data: Данные, передаваемые в обработчик.
        :return: Результат выполнения обработчика.
        """
        logger.debug(f"Получаем событие. Тип события {type(event)}")

        message: Message = event.message
        if message.text.startswith("/"):
            logger.debug(f"Событие - это команда {message.text}. "
                         f"Обрабатываем ее.")
            return await handler(event, data)

        logger.debug("Событие - это потенциальный IMEI. "
                     "Обрабатываем его.")

        tg_id = message.from_user.id

        if not await self.check_user(tg_id=tg_id):
            logger.debug(f"Пользователя {tg_id} нет в белом списке. "
                         f"Отказываем.")
            data["answer"] = (
                "Недостаточно прав на использование бота. "
                "Обратитесь к @fantasynick"
            )

            return await handler(event, data)

        imei = message.text
        logger.debug(f"Запуск валидации IMEI: {imei}")
        validated_imei = self.validation(imei=imei)

        if isinstance(validated_imei, IMEIValidator):
            logger.debug("Валидация прошла успешно. "
                         "Делаем запрос по API.")

            response = await get_imei_info(
                imei=message.text,
                url=self.imeicheck_url,
                token=self.imeicheck_token.get_secret_value(),
            )

            file_path = await self.write_answer(data=response, imei=imei)
            data["answer"] = file_path
        else:
            logger.debug("Валидация прошла не успешно. "
                         "Возвращаем ошибку.")

            err = validated_imei.errors()[0]["ctx"]["error"].args[0]
            data["answer"] = str(err)

        return await handler(event, data)

    async def check_user(self, tg_id: int) -> bool:
        """
        Проверяет, есть ли пользователь с переданным id в бд.

        :param tg_id: Id пользователя.
        :return: True, если пользователь есть и False если нет.
        """

        async with self.session as session:
            user = await self.repository.read(session=session, tg_id=tg_id)
        if not user:
            return False

        return True

    @staticmethod
    def validation(imei: str) -> IMEIValidator | pydantic.ValidationError:
        """
        Валидирует imei на корректность.

        :param imei: Запрошенный imei.
        :return: Валидированный imei или ошибку.
        """
        try:
            validated_imei = IMEIValidator(imei=imei)
            return validated_imei

        except pydantic.ValidationError as exc:
            return exc

    @staticmethod
    async def write_answer(data: json, imei: str) -> str:
        """
        Записывает ответ в файл и возвращает путь к нему.

        :param data: Ответ от API.
        :param imei: Запрошенный imei.
        :return: Путь до файла.
        """
        logger.debug("Записываем данные в файл.")
        folder_path = os.path.abspath(os.path.join("app", "static", "reports"))
        file_path = os.path.join(folder_path, f"{imei}.json")

        os.makedirs(folder_path, exist_ok=True)

        async with aiofiles.open(file_path, "w", encoding="utf-8") as file:
            await file.write(json.dumps(data, indent=2, ensure_ascii=False))

        logger.debug(f"Успех. Путь до файла: {file_path}")

        return file_path
