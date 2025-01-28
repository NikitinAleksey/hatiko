from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

__all__ = ["commands_router"]

commands_router = Router()


@commands_router.message(CommandStart())
async def start_handler(message: Message):
    """
    Обработчик команды /start.

    :param message: Сообщение от пользователя.
    :return: Ответное сообщение.
    """
    await message.answer(
        text="Привет! Этот бот умеет проверять IMEI твоего устройства. "
        "Для проверки просто отправь IMEI. "
        "Но помни, что ты должен быть в списке тех, кому доступен бот.",
    )
