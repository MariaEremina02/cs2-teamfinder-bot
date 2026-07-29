#База данных CS2 TeamFinder Bot.
#Модель User + CRUD-функции.
#ИспользуюSQLAlchemy + PostgreSQL.


from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
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



# CRUD-ФУНКЦИИ

def create_user(telegram_id: int, username: str = None) -> User:

#Создание нового пользователя в базе данных
#Возвращает созданного пользователя

    with Session(engine) as session:
        user = User(telegram_id=telegram_id, username=username)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user(telegram_id: int) -> User | None:

#Поиск пользователя по Telegram ID
#Возвращает пользователя или None, если не найден

    with Session(engine) as session:
        return session.query(User).filter_by(telegram_id=telegram_id).first()


def get_or_create_user(telegram_id: int, username: str = None) -> User:

#Поиск пользователя по Telegram ID
#Если не найден — создать нового
#Возвращает пользователя

    user = get_user(telegram_id)
    if user is None:
        user = create_user(telegram_id, username)
    return user


def update_user(telegram_id: int, rank: str = None, play_time: str = None) -> User | None:

#Обновление данных пользователя (звание и/или время игры)
#Возвращает обновлённого пользователя или None, если не найден

    with Session(engine) as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            if rank is not None:
                user.rank = rank
            if play_time is not None:
                user.play_time = play_time
            session.commit()
            session.refresh(user)
        return user


def find_teammates(telegram_id: int, rank: str) -> list[type[User]]:

#Поиск активных игроков с таким же званием (кроме самого пользователя)
#Возвращает список пользователей

    with Session(engine) as session:
        return (
            session.query(User)
            .filter(
                User.rank == rank,
                User.telegram_id != telegram_id,
                User.is_active == True
            )
            .all()
        )


def deactivate_user(telegram_id: int) -> User | None:

#Деактивация профиля пользователя (is_active = False)
#Возвращает обновлённого пользователя или None

    with Session(engine) as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user:
            user.is_active = False
            session.commit()
            session.refresh(user)
        return user

# Возврат общего количества зарегистрированных пользователей
def get_total_users_count() -> int:

    with Session(engine) as session:
        return session.query(User).count()

# Возврат количества активных пользователей
def get_active_users_count() -> int:

    with Session(engine) as session:
        return session.query(User).filter_by(is_active=True).count()
