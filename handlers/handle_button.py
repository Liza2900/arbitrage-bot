from telegram import Update
from telegram.ext import ContextTypes
from arbitrage import find_arbitrage_opportunities

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "find_arbitrage":
        await query.edit_message_text("🔄 Шукаю можливості арбітражу...")
        opportunities = await find_arbitrage_opportunities()

        if not opportunities:
            text = "Нічого не знайдено ❌"
        else:
            lines = []
            for opp in opportunities:
                lines.append(
                    f"💰 {opp['symbol']}\n"
                    f"Купити на {opp['buy']['exchange']} за {opp['buy']['price']:.4f} USDT\n"
                    f"Продати на {opp['sell']['exchange']} за {opp['sell']['price']:.4f} USDT\n"
                    f"Профіт: {opp['spread_percent']}%\n"
                )
            text = "\n".join(lines)

        await context.bot.send_message(chat_id=query.message.chat_id, text=text)
