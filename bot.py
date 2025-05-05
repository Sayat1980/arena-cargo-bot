import os
import pandas as pd
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")
csv_url = "https://raw.githubusercontent.com/Sayat1980/arena-cargo-bot/main/tracking.csv"

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Показать статус по треку", callback_data="get_status")],
        [InlineKeyboardButton("Перейти на канал", url="https://t.me/arenacargo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_status":
        user_states[query.from_user.id] = "awaiting_track"
        await query.message.reply_text("Пожалуйста, введите номер трека:")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_states.get(user_id) == "awaiting_track":
        track_number = update.message.text.strip()
        try:
            df = pd.read_csv(csv_url, encoding="utf-8-sig")
            df.columns = df.columns.str.strip()  # удалить лишние пробелы в заголовках

            if "TrackNumber" not in df.columns or "Status" not in df.columns:
                await update.message.reply_text("Файл не содержит нужных колонок.")
                return

            match = df[df["TrackNumber"] == track_number]
            if not match.empty:
                status = match.iloc[0]["Status"]
                await update.message.reply_text(f"Статус: {status}")
            else:
                await update.message.reply_text("Трек-номер не найден.")
        except Exception as e:
            await update.message.reply_text(f"Ошибка при чтении файла: {e}")
        finally:
            user_states[user_id] = None

if _name_ == "_main_":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()
