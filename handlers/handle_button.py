async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_arbitrage":
        await query.edit_message_text("🔄 Шукаю можливості арбітражу...")
        try:
            result = await find_arbitrage_opportunities()
            text = format_opportunities(result)
        except Exception as e:
            text = f"❌ Виникла помилка: {e}"
        await context.bot.send_message(chat_id=query.message.chat_id, text=text[:4000], parse_mode="HTML")
