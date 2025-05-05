from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
import os
import pandas as pd

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать статус", callback_data="show_status")],
        [InlineKeyboardButton("Перейти в канал", url="https://t.me/arenacargo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Обработка нажатия на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "show_status":
        await query.edit_message_text("Введите номер трека:")

# Обработка текстового ввода (номер трека)
async def handle_track_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_number = update.message.text.strip()
    try:
        df = pd.read_csv("tracking.csv")
        result = df[df["TrackNumber"] == track_number]
        if not result.empty:
            status = result.iloc[0]["Status"]
            await update.message.reply_text(f"Статус для {track_number}: {status}")
        else:
            await update.message.reply_text("Трек-номер не найден.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при чтении файла: {e}")

# Запуск приложения
app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_track_query))

app.run_polling()
