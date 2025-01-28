from pathlib import Path

from aiogram import Router
from aiogram.types import FSInputFile, Message

from app.services.logger.logger import AppLogger

__all__ = ["imeicheck_router"]

imeicheck_router = Router()

logger = AppLogger("imeicheck")


@imeicheck_router.message()
async def imeicheck_handler(message: Message, answer: str):
    logger.debug(f"Зашли в хендлер и получили данные: {answer}")
    if Path(answer).is_file():
        await message.answer_document(FSInputFile(answer))
    else:
        await message.answer(text=answer)
