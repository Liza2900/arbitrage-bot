from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # або встав токен напряму

# Telegram application
telegram_app = Application.builder().token(BOT_TOKEN).build()

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Бот працює.")

telegram_app.add_handler(CommandHandler("start", start))

@app.on_event("startup")
async def on_startup():
    await telegram_app.initialize()
    await telegram_app.start()

@app.on_event("shutdown")
async def on_shutdown():
    await telegram_app.stop()

@app.get("/")
async def root():
    return {"message": "Arbitrage Bot is running."}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}
