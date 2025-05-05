import os
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

FILE_NAME = "tracking.csv"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь трек-номер, чтобы сохранить его.")

async def save_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([number])
    await update.message.reply_text(f"Сохранил трек-номер: {number}")

async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(FILE_NAME):
        await update.message.reply_text("Нет сохраненных треков.")
        return
    with open(FILE_NAME, "r") as file:
        content = file.read()
    await update.message.reply_text(content or "Файл пуст.")

app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("all", show_all))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_tracking))

app.run_polling()
