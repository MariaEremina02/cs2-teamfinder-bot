import pytest
from sqlalchemy.orm import Session
from database import (
    get_test_engine,
    User,
    create_user,
    get_user,
    update_user,
    find_teammates,
    get_top_ranks,
    delete_user,
)

# Чистая БД для каждого теста
@pytest.fixture
def session():

    engine = get_test_engine()
    with Session(engine) as s:
        yield s


def test_create_user(session):
    user = create_user(telegram_id=12345, username="test_user", session=session)
    assert user.telegram_id == 12345
    assert user.username == "test_user"


def test_get_user(session):
    create_user(telegram_id=11111, username="player1", session=session)
    assert get_user(11111, session=session) is not None
    assert get_user(99999, session=session) is None


def test_update_user(session):
    create_user(telegram_id=22222, username="player2", session=session)
    update_user(22222, rank="Silver IV", play_time="Вечер", session=session)
    user = get_user(22222, session=session)
    assert user.rank == "Silver IV"
    assert user.play_time == "Вечер"


def test_find_teammates(session):
    for tid in [1, 2, 3]:
        create_user(telegram_id=tid, session=session)
    update_user(1, rank="Silver IV", play_time="Утро", session=session)
    update_user(2, rank="Silver IV", play_time="Вечер", session=session)
    update_user(3, rank="Gold Nova I", play_time="Ночь", session=session)

    teammates = find_teammates(1, "Silver IV", session=session)
    assert len(teammates) == 1
    assert teammates[0].telegram_id == 2


def test_get_top_ranks(session):
    data = [(10, "Silver IV"), (20, "Silver IV"), (30, "Silver IV"),
            (40, "Gold Nova I"), (50, "Gold Nova I"), (60, "Global Elite")]
    for tid, rank in data:
        create_user(telegram_id=tid, session=session)
        update_user(tid, rank=rank, play_time="Вечер", session=session)
    top = get_top_ranks(session=session)
    assert top[0] == ("Silver IV", 3)
    assert top[1] == ("Gold Nova I", 2)


def test_delete_user(session):
    create_user(telegram_id=77777, session=session)
    assert delete_user(77777, session=session) is True
    assert get_user(77777, session=session) is None
    assert delete_user(99999, session=session) is False