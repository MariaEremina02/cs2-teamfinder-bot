import asyncio
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from config import BOT_TOKEN
from handlers import (
    start,
    choose_group,
    choose_rank,
    choose_time,
    back_to_groups,
    show_profile,
    change_profile,
    find_teammates_handler,
    unknown_message,
    stats,
    show_help,
    top_ranks,
    delete_profile,
    confirm_delete,
    cancel_delete,
)
from states import CHOOSING_GROUP, CHOOSING_RANK, CHOOSING_TIME

#Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main():
#Запуск бота
    logger.info("🤖 Запускаем CS2 TeamFinder Bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ConversationHandler для регистрации и изменения профиля
    registration_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^✏️ Изменить профиль$"), change_profile),
        ],
        states={
            CHOOSING_GROUP: [CallbackQueryHandler(choose_group, pattern="^group:")],
            CHOOSING_RANK: [
                CallbackQueryHandler(choose_rank, pattern="^rank:"),
                CallbackQueryHandler(back_to_groups, pattern="^back_to_groups$"),
            ],
            CHOOSING_TIME: [CallbackQueryHandler(choose_time, pattern="^time:")],
        },
        fallbacks=[],
    )

    app.add_handler(registration_handler)

    # Обработчики главного меню
    app.add_handler(MessageHandler(filters.Regex("^👤 Мой профиль$"), show_profile))
    app.add_handler(MessageHandler(filters.Regex("^🔍 Найти тиммейтов$"), find_teammates_handler))
    app.add_handler(MessageHandler(filters.Regex("^ℹ️ Помощь$"), show_help))
    app.add_handler(CommandHandler("top", top_ranks))
    app.add_handler(MessageHandler(filters.Regex("^🗑 Удалить профиль$"), delete_profile))
    app.add_handler(CallbackQueryHandler(confirm_delete, pattern="^confirm_delete$"))
    app.add_handler(CallbackQueryHandler(cancel_delete, pattern="^cancel_delete$"))


    # Обработчик неизвестных сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message))

    # Команда /stats
    app.add_handler(CommandHandler("stats", stats))

    logger.info("✅ Бот запущен! Нажмите Ctrl+C для остановки.")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Бот остановлен.")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
