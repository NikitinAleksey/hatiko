import asyncio
import json

import aiohttp

from app.services.logger.logger import AppLogger

__all__ = ["get_imei_info"]

logger = AppLogger("get_imei_info")


async def get_imei_info(imei: str, url: str, token: str) -> str | None:
    logger.debug(f"Делаем запрос к API. IMEI: {imei}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = json.dumps({
        "deviceId": imei,
        "serviceId": 1
    })

    timeout = aiohttp.ClientTimeout(total=10)
    data = None

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(
                    url=url,
                    headers=headers,
                    data=body
            ) as response:
                data = await response.json()

        except asyncio.TimeoutError:
            data = ("Время ожидания ответа истекло, "
                    "попробуйте позже.")
        except Exception:
            data = response.text()

    logger.debug("Запрос успешен, есть ответ.")
    return data
