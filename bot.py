from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes, ConversationHandler
import csv

# Токен бота
TOKEN = '7711800920:AAFHz_sA0QwWGK5qHRT0qvKYlNfkUOtMxWs'

# Состояние для отслеживания
ASK_TRACKING = 1

# Загрузка данных из CSV
def load_tracking_data():
    data = {}
    try:
        with open('tracking.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) >= 2:
                    data[row[0].strip()] = row[1].strip()
    except FileNotFoundError:
        print("⚠️ Файл tracking.csv не найден.")
    return data

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Посмотреть статус товара", callback_data='check_status')],
        [InlineKeyboardButton("📣 Канал Arena Cargo", url="https://t.me/arenacargo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать в Arena Cargo!", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'check_status':
        await query.message.reply_text("Пожалуйста, введите ваш трек-номер:")
        return ASK_TRACKING

# Получение трек-номера
async def receive_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tracking_code = update.message.text.strip()
    data = load_tracking_data()
    status = data.get(tracking_code, '❌ Трек-номер не найден. Проверьте правильность.')
    await update.message.reply_text(f'📦 Статус товара:\n{status}')
    return ConversationHandler.END

# Основной запуск
def main():
    print("🚀 Бот запущен...")
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler)],
        states={ASK_TRACKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_tracking)]},
        fallbacks=[]
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv_handler)

    # Webhook URL
WEBHOOK_HOST = os.getenv("WEBHOOK_URL")  # Пример: https://your-app.up.railway.app
WEBHOOK_PATH = f"/{os.getenv('TOKEN')}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get('PORT', 8000)),
    webhook_url=WEBHOOK_URL
)
if __name__ == '__main__':
    main()
