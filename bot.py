from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os
import csv

# Функция обработки кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "show_statuses":
        response = ""
        try:
            with open("tracking.csv", newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 2:
                        response += f"{row[0]} — {row[1]}\n"
        except FileNotFoundError:
            response = "Файл tracking.csv не найден."
        await query.edit_message_text(text=response or "Нет данных.")
    
    elif query.data == "goto_channel":
        await query.edit_message_text(text="Перейдите в наш канал: https://t.me/arenacargo")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать статусы", callback_data="show_statuses")],
        [InlineKeyboardButton("Канал ArenaCargo", callback_data="goto_channel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Запуск бота
app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
