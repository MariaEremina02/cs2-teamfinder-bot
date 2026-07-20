import asyncio
import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update, context):

    # Обработчик команды /start

    user = update.effective_user
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n"
        f"Я CS2 Team Finder Bot.\n"
        f"Помогу найти тиммейтов твоего уровня.\n\n"
        f"Скоро здесь будет регистрация."
    )


async def main():

    logger.info("🤖 Запускаем CS2 TeamFinder Bot...")

    # Создание приложения
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрация обработчика команды /start
    app.add_handler(CommandHandler("start", start))

    logger.info("✅ Бот запущен! Нажмите Ctrl+C для остановки.")

    # Запуск бота
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    # Тут я держу бота запущенным
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
