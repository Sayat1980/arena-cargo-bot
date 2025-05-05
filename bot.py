import os
import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

DATA_FILE = 'tracking.csv'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для отслеживания посылок.")

async def add_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tracking_number = ' '.join(context.args)
    if not tracking_number:
        await update.message.reply_text("Укажите номер трека после команды /add")
        return

    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([tracking_number])

    await update.message.reply_text(f"Трек-номер {tracking_number} сохранён.")

app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_tracking))
app.run_polling()
