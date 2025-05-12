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


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 Знайти арбітраж", callback_data="find_arbitrage")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Натисни кнопку для пошуку арбітражу:", reply_markup=reply_markup)


# Обробка кнопки
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if __name__ == "__main__":
    import uvicorn
    uvicorn.run("arbitrage_bot_fastapi:app", host="0.0.0.0", port=8080)


    if query.data == "find_arbitrage":
        await query.edit_message_text("🔄 Шукаю можливості арбітражу...")
        result = await find_arbitrage_opportunities()
        text = result if result else "Нічого не знайдено ❌"
        await context.bot.send_message(chat_id=query.message.chat_id, text=text)


# Додаємо хендлери
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(handle_button))


# FastAPI стартова сторінка
@app.get("/")
async def root():
    return {"message": "Arbitrage Bot is running."}


# Обробка webhook запитів від Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)


# Старт додатку та webhook
@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
    await application.start()
