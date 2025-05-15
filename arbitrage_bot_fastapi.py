import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from arbitrage import find_arbitrage_opportunities
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Наприклад: https://your-bot-name.onrender.com

app = FastAPI()
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

# Форматування арбітражних можливостей
def format_opportunities(opps):
    if not opps:
        return "Нічого не знайдено ❌"

    lines = []
    for o in opps:
        lines.append(
            f"💰 <b>{o['symbol']}</b>\n"
            f"Купити: <b>{o['buy']['exchange']}</b> — {o['buy']['price']}$\n"
            f"Продати: <b>{o['sell']['exchange']}</b> — {o['sell']['price']}$\n"
            f"📈 Спред: <b>{o['spread_percent']}%</b>\n"
        )
    return "\n".join(lines)


# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Знайти арбітраж", callback_data="find_arbitrage")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Натисни кнопку для пошуку арбітражу:", reply_markup=reply_markup)


# Обробка кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_arbitrage":
        await query.edit_message_text("🔄 Шукаю можливості арбітражу...")
        result = await find_arbitrage_opportunities()
        text = format_opportunities(result)
        await context.bot.send_message(chat_id=query.message.chat_id, text=text[:4000], parse_mode="HTML")


# Додаємо хендлери
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_button))


# Коренева сторінка FastAPI
@app.get("/")
async def root():
    return {"message": "Arbitrage Bot is running."}


# Обробка вхідних webhook-запитів від Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)


# Ініціалізація бота та встановлення webhook
@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
