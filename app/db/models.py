from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["WhileUsersList"]

Base = declarative_base()


class WhileUsersList(Base):
    __tablename__ = "users"
    """
    Модель белого списка пользователей.

    :param id: Int - уникальный идентификатор записи.
    :param user_id: Int - идентификатор пользователя в Telegram.
    """

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
