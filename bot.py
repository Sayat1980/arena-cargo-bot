from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот Arena Cargo и работаю через webhook!")

# Создание приложения с токеном
app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

# Добавление обработчика команды
app.add_handler(CommandHandler("start", start))

# Получение адреса webhook
WEBHOOK_HOST = os.getenv("WEBHOOK_URL")  # например: https://arena-cargo-bot.up.railway.app
WEBHOOK_PATH = f"/{os.getenv('TOKEN')}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Запуск webhook-сервера
app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8000)),
    webhook_url=WEBHOOK_URL
)