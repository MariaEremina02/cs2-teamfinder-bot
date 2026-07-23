import asyncio
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler
from config import BOT_TOKEN
from handlers import start, choose_group, choose_rank, choose_time, back_to_groups
from states import CHOOSING_GROUP, CHOOSING_RANK, CHOOSING_TIME

#Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main(update):

#Обработчик команды /start

    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n"
        f"Я CS2 Team Finder Bot.\n"
        f"Помогу найти тиммейтов твоего уровня.\n\n"
        f"Скоро здесь будет регистрация."
    )


async def main():

#Запуск бота
    logger.info("🤖 Запускаем CS2 TeamFinder Bot...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

#ConversationHandler для регистрации
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
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
