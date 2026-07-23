#Обработчики команд и кнопок бота
#Регистрация, профиль, поиск тиммейтов


from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database import get_or_create_user, update_user
from keyboards import (
    get_group_keyboard,
    get_rank_keyboard,
    get_time_keyboard,
    get_main_menu_keyboard,
)
from states import CHOOSING_GROUP, CHOOSING_RANK, CHOOSING_TIME



#Команда /start — начало регистрации


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.effective_user

#Создание и приветствие пользователя в БД (если его ещё нет)
    get_or_create_user(user.id, user.username)

    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"Я помогу найти тиммейтов для CS2.\n"
        f"Давай создадим твой профиль :)\n\n"
        f"Шаг 1/3: Выбери группу своего звания:",
        reply_markup=get_group_keyboard(),
    )
    return CHOOSING_GROUP



#Первый шаг: выбор группы рангов


async def choose_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

#Сохранение группы, показ и выбор конкретного звания

    query = update.callback_query
    await query.answer()

    group = query.data.replace("group:", "")
    context.user_data["group"] = group

    await query.edit_message_text(
        f"Шаг 2/3: Ты выбрал группу «{group}».\n"
        f"Теперь выбери конкретное звание:",
        reply_markup=get_rank_keyboard(group),
    )
    return CHOOSING_RANK



#Кнопка "НАЗАД"


async def back_to_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

#Возврат к выбору группы рангов

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "Шаг 1/3: Выбери группу своего звания:",
        reply_markup=get_group_keyboard(),
    )
    return CHOOSING_GROUP



#Второй шаг: выбор конкретного звания


async def choose_rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

#Сохранение, показ и выбор времени

    query = update.callback_query
    await query.answer()

    rank = query.data.replace("rank:", "")
    context.user_data["rank"] = rank

    await query.edit_message_text(
        f"Шаг 3/3: Твоё звание — «{rank}».\n"
        f"В какое время ты обычно играешь?",
        reply_markup=get_time_keyboard(),
    )
    return CHOOSING_TIME



#Третий шаг: выбор времени и завершение регистрации


async def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

#Сохранение в БД и показ главное меню

    query = update.callback_query
    await query.answer()

    play_time = query.data.replace("time:", "")
    user_id = update.effective_user.id

#Сохранение в БД
    update_user(user_id, rank=context.user_data["rank"], play_time=play_time)

    await query.edit_message_text(
        f"✅ Профиль создан!\n\n"
        f"👤 Звание: {context.user_data['rank']}\n"
        f"🕐 Время игры: {play_time}\n\n"
        f"Теперь ты можешь искать тиммейтов ^_^",
    )

#Отправка пользователя в главное меню
    await query.message.reply_text(
        "Что хочешь сделать?",
        reply_markup=get_main_menu_keyboard(),
    )

    return ConversationHandler.END