#База данных CS2 TeamFinder Bot
#Модель User + CRUD-функции
#Использую SQLAlchemy + PostgreSQL

from typing import Any

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime

DATABASE_URL = "postgresql+psycopg://posgres:postgres@localhost:5432/cs2_bot"

#Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)


#Базовая модель для всех таблиц
class Base(DeclarativeBase):
    pass


#Модель USER (таблица пользователей)


class User(Base):
#Таблица пользователей бота
#Хранит Telegram ID, username, звание, время игры

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False, comment="Telegram ID пользователя")
    username = Column(String, nullable=True, comment="@username в Telegram")
    rank = Column(String, nullable=True, comment="Звание в CS2 (например, Silver IV)")
    play_time = Column(String, nullable=True, comment="Время игры (Утро/День, Вечер, Ночь)")
    is_active = Column(Boolean, default=True, comment="Активен ли профиль")
    created_at = Column(DateTime, default=datetime.now, comment="Дата создания профиля")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, rank={self.rank})>"


#СОЗДАНИЕ ТАБЛИЦ


#Автоматическое создание всех таблиц (если их ещё нет)
Base.metadata.create_all(engine)


#CRUD-ФУНКЦИИ

def create_user(telegram_id: int, username: str = None, session=None) -> User:
#Создание нового пользователя в базе данных
#Возвращает созданного пользователя
#session=None — если не передана, создаётся своя сессия

    if session is None:
        with Session(engine) as s:
            user = User(telegram_id=telegram_id, username=username)
            s.add(user)
            s.commit()
            s.refresh(user)
            return user
    else:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user(telegram_id: int, session=None) -> User | None:
#Поиск пользователя по Telegram ID
#Возвращает пользователя или None, если не найден

    if session is None:
        with Session(engine) as s:
            return s.query(User).filter_by(telegram_id=telegram_id).first()
    else:
        return session.query(User).filter_by(telegram_id=telegram_id).first()


def get_or_create_user(telegram_id: int, username: str = None, session=None) -> User:
#Поиск пользователя по Telegram ID
#Если не найден — создать нового
#Возвращает пользователя

    user = get_user(telegram_id, session=session)
    if user is None:
        user = create_user(telegram_id, username, session=session)
    return user


def update_user(telegram_id: int, rank: str = None, play_time: str = None, session=None) -> User | None:
#Обновление данных пользователя (звание и/или время игры)
#Возвращает обновлённого пользователя или None, если не найден

    if session is None:
        with Session(engine) as s:
            user = s.query(User).filter_by(telegram_id=telegram_id).first()
            if user:
                if rank is not None:
                    user.rank = rank
                if play_time is not None:
                    user.play_time = play_time
                s.commit()
                s.refresh(user)
            return user
    else:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            if rank is not None:
                user.rank = rank
            if play_time is not None:
                user.play_time = play_time
            session.commit()
            session.refresh(user)
        return user


def find_teammates(telegram_id: int, rank: str, session=None) -> list[User]:

#Поиск активных игроков с таким же званием (кроме самого пользователя)
#Возвращает список пользователей

    if session is None:
        with Session(engine) as s:
            return s.query(User).filter(
                User.rank == rank,
                User.telegram_id != telegram_id,
                User.is_active == True
            ).all()
    else:
        return session.query(User).filter(
            User.rank == rank,
            User.telegram_id != telegram_id,
            User.is_active == True
        ).all()


def deactivate_user(telegram_id: int, session=None) -> User | None:
#Деактивация профиля пользователя (is_active = False)
#Возвращает обновлённого пользователя или None

    if session is None:
        with Session(engine) as s:
            user = s.query(User).filter_by(telegram_id=telegram_id).first()
            if user:
                user.is_active = False
                s.commit()
                s.refresh(user)
            return user
    else:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            user.is_active = False
            session.commit()
            session.refresh(user)
        return user


# Возврат общего количества зарегистрированных пользователей
def get_total_users_count(session=None) -> int:
    if session is None:
        with Session(engine) as s:
            return s.query(User).count()
    else:
        return session.query(User).count()


# Возврат количества активных пользователей
def get_active_users_count(session=None) -> int:
    if session is None:
        with Session(engine) as s:
            return s.query(User).filter_by(is_active=True).count()
    else:
        return session.query(User).filter_by(is_active=True).count()


# Топ званий по кол-ву пользователей (по убыванию)
def get_top_ranks(session=None) -> list[tuple[str, int]]:
    if session is None:
        with Session(engine) as s:
            results = (
                s.query(User.rank, func.count(User.id))
                .filter(User.rank.isnot(None))
                .group_by(User.rank)
                .order_by(func.count(User.id).desc())
                .limit(10)
                .all()
            )
            return results
    else:
        results = (
            session.query(User.rank, func.count(User.id))
            .filter(User.rank.isnot(None))
            .group_by(User.rank)
            .order_by(func.count(User.id).desc())
            .limit(10)
            .all()
        )
        return results


# Удаление пользователя из БД
def delete_user(telegram_id: int, session=None) -> bool:
    if session is None:
        with Session(engine) as s:
            user = s.query(User).filter_by(telegram_id=telegram_id).first()
            if user:
                s.delete(user)
                s.commit()
                return True
            return False
    else:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            session.delete(user)
            session.commit()
            return True
        return False


# Тестовая БД. Создание временной БД для тестов
def get_test_engine():
    from sqlalchemy import create_engine
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(test_engine)
    return test_engine