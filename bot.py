import os
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Команда /start — показывает две кнопки
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать статусы", callback_data="show_status")],
        [InlineKeyboardButton("Канал ArenaCargo", url="https://t.me/arenacargo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Обработка нажатий по кнопкам
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "show_status":
        try:
            df = pd.read_csv("tracking.csv")
            if df.empty:
                text = "Файл tracking.csv пуст."
            else:
                text = "\n".join(f"{row['TrackNumber']}: {row['Status']}" for _, row in df.iterrows())
            await query.edit_message_text(f"Статусы треков:\n\n{text}")
        except Exception as e:
            await query.edit_message_text(f"Ошибка при чтении файла: {e}")

# Запуск бота
app = ApplicationBuilder().token(os.getenv("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()