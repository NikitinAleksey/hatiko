from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import WhileUsersList

__all__ = ["WhileUsersListRepository"]


class WhileUsersListRepository:
    _model = WhileUsersList

    @classmethod
    async def create(
        cls, session: AsyncSession, item: WhileUsersList
    ) -> WhileUsersList:
        """
        Создает новый элемент в базе данных.

        :param session: AsyncSession - асинхронная сессия
        для работы с базой данных.
        :param item: WhileUsersList - объект для сохранения в базе данных.
        :return: Item: Сохраненный объект.
        """
        session.add(item)
        await session.commit()
        return item

    @classmethod
    async def read(
            cls, session: AsyncSession,
            tg_id: int
    ) -> None | WhileUsersList:
        """
        Читает данные из базы данных по tg_id и модели.

        :param session: AsyncSession - асинхронная сессия
        для работы с базой данных.
        :param tg_id: Int - ID пользователя Telegram.
        :return: Объект модели или None, если данные не найдены.
        """
        stmt = select(cls._model).where(cls._model.user_id == tg_id)
        result = await session.execute(stmt)
        return result.scalars().first()

    @classmethod
    async def update(
        cls, session: AsyncSession, item: WhileUsersList
    ) -> WhileUsersList:
        """
        Обновляет данные элемента в базе данных.

        :param session: AsyncSession - асинхронная сессия
        для работы с базой данных.
        :param item: WhileUsersList - объект с обновленными данными.
        :return: WhileUsersList - объект модели.
        """
        merged_item = await session.merge(item)
        await session.commit()
        return merged_item

    @classmethod
    async def delete(
        cls, session: AsyncSession, item: WhileUsersList
    ) -> WhileUsersList:
        """
        Удаляет элемент из базы данных.

        :param session: AsyncSession - асинхронная сессия
        для работы с базой данных.
        :param item: WhileUsersList - объект, который необходимо удалить.
        :return: WhileUsersList.
        """
        await session.delete(item)
        await session.commit()
        return item
