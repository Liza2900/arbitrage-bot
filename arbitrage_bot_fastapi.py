from fastapi import FastAPI, Request
import httpx
import os
from arbitrage import find_arbitrage_opportunities
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

app = FastAPI()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET_PATH = "/webhook"

# FastAPI endpoint for Telegram webhook
@app.post(WEBHOOK_SECRET_PATH)
async def telegram_webhook(request: Request):
    update_data = await request.json()
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Arbitrage Bot is running."}

# --- Telegram Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Знайти арбітраж", callback_data="find_arbitrage")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Натисни кнопку нижче, щоб знайти арбітражні можливості:", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_arbitrage":
        result = await find_arbitrage_opportunities()
        message = result if result else "Арбітражні можливості не знайдені."
        await query.edit_message_text(text=message)

# --- Ініціалізація Telegram Application ---
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_button))
