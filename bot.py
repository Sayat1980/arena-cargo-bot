from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот Arena Cargo и работаю через polling!")

# Создание приложения с токеном
app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

# Регистрация команды
app.add_handler(CommandHandler("start", start))

# Запуск бота в режиме polling
app.run_polling()
