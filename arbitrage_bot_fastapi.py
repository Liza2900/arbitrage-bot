import os
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

from arbitrage import find_arbitrage_opportunities

TOKEN = os.getenv("BOT_TOKEN")  # додай в Render як змінну середовища
WEBHOOK_PATH = f"/webhook/{TOKEN}"

app = FastAPI()
bot_app = Application.builder().token(TOKEN).build()

# Стартова команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 Знайти арбітраж", callback_data="find_arbitrage")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Натисни кнопку нижче, щоб знайти арбітражні можливості:", reply_markup=reply_markup)

# Обробка кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("Шукаю арбітражні можливості...")
    result = await find_arbitrage_opportunities()

    if not result:
        await query.message.reply_text("Нічого не знайдено.")
    else:
        text = "\n\n".join(result)
        await query.message.reply_text(f"🔁 Знайдено:\n\n{text}")

# Додаємо хендлери
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(handle_button))

# Webhook endpoint
@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"ok": True}

# Проста перевірка
@app.get("/")
async def root():
    return {"message": "Arbitrage bot is running via webhook"}
