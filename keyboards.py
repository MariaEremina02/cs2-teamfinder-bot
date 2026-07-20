#Клавиатуры для CS2 TeamFinder Bot.
#Inline-клавиатуры для выбора ранга (двухшаговая)
#Reply-клавиатура для главного меню


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from rank_data import RANK_GROUPS, RANKS_BY_GROUP, PLAY_TIMES



#Клавиатура для выбора рангов (шаг 1 регистрации)


def get_group_keyboard() -> InlineKeyboardMarkup:

#Создание inline-клавиатуры с 5 группами рангов
#Каждая кнопка — группа (Silver, Gold Nova и т.д.)

    keyboard = []
    for group in RANK_GROUPS:
        keyboard.append([InlineKeyboardButton(group, callback_data=f"group:{group}")])
    return InlineKeyboardMarkup(keyboard)



#Клавиатура для выбора конкретного звания (шаг 2 регистрации)


def get_rank_keyboard(group: str) -> InlineKeyboardMarkup:

#Создание inline-клавиатуры с конкретными званиями выбранной группы
#И кнопка «Назад» для возврата к выбору группы

    keyboard = []
    for rank in RANKS_BY_GROUP[group]:
        keyboard.append([InlineKeyboardButton(rank, callback_data=f"rank:{rank}")])
#Кнопка возврата
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_groups")])
    return InlineKeyboardMarkup(keyboard)



#Клавиатура для выбора времени игры (шаг 3 регистрации)


def get_time_keyboard() -> InlineKeyboardMarkup:

#Создание inline-клавиатуры с 3 вариантами времени игры

    keyboard = []
    for time in PLAY_TIMES:
        keyboard.append([InlineKeyboardButton(time, callback_data=f"time:{time}")])
    return InlineKeyboardMarkup(keyboard)



#После регистрации появляется главное меню, а именно:


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:

#Создание reply-клавиатуры главного меню с тремя кнопками

    keyboard = [
        [KeyboardButton("🔍 Найти тиммейтов")],
        [KeyboardButton("👤 Мой профиль")],
        [KeyboardButton("✏️ Изменить профиль")],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,  #Кнопки подгоняются под экран
        one_time_keyboard=False,  #Клавиатура не скрывается после нажатия
    )