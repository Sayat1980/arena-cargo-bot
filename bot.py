from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters, ConversationHandler
)
import os
import pandas as pd

# Этапы диалога
WAITING_TRACK = 1

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать статус по треку", callback_data="status")],
        [InlineKeyboardButton("Перейти на канал", url="https://t.me/arenacargo")]
    ]
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "status":
        await query.message.reply_text("Пожалуйста, введите номер трека:")
        return WAITING_TRACK

# Обработка введённого трек-номера
async def track_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_number = update.message.text.strip()

    try:
        df = pd.read_csv("tracking.csv")
        df.columns = df.columns.str.strip()  # убрать лишние пробелы

        if "TrackNumber" not in df.columns or "Status" not in df.columns:
            await update.message.reply_text("Файл не содержит нужных колонок.")
            return ConversationHandler.END

        result = df[df["TrackNumber"].astype(str).str.strip() == track_number]

        if not result.empty:
            status = result.iloc[0]["Status"]
            await update.message.reply_text(f"Статус трека {track_number}: {status}")
        else:
            await update.message.reply_text(f"Трек-номер {track_number} не найден.")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при чтении файла: {e}")

    return ConversationHandler.END

# Запуск бота
if _name_ == "_main_":
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={WAITING_TRACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, track_status)]},
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()
