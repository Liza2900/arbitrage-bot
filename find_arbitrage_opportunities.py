import logging
from exchanges.bitget import get_bitget_prices
from exchanges.kucoin import get_kucoin_prices
from exchanges.okx import get_okx_prices
from exchanges.mexc import get_mexc_prices
from exchanges.bingx import get_bingx_prices

# 🔽 Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PROFIT_THRESHOLD = 0.8  # відсоток
PRICE_LIMIT = 15        # не брати монети дорожче цього
VOLUME_LIMIT = 10       # не брати монети з меншим обсягом

async def find_arbitrage_opportunities():
    bitget = kucoin = okx = mexc = bingx = {}

    try:
        bitget = await get_bitget_prices()
        logging.info(f"✅ Bitget: отримано {len(bitget)} монет")
    except Exception:
        logging.exception("❌ Помилка при отриманні цін з Bitget")

    try:
        kucoin = await get_kucoin_prices()
        logging.info(f"✅ Kucoin: отримано {len(kucoin)} монет")
    except Exception:
        logging.exception("❌ Помилка при отриманні цін з Kucoin")

    try:
        okx = await get_okx_prices()
        logging.info(f"✅ OKX: отримано {len(okx)} монет")
    except Exception:
        logging.exception("❌ Помилка при отриманні цін з OKX")

    try:
        mexc = await get_mexc_prices()
        logging.info(f"✅ MEXC: отримано {len(mexc)} монет")
    except Exception:
        logging.exception("❌ Помилка при отриманні цін з MEXC")

    try:
        bingx = await get_bingx_prices()
        logging.info(f"✅ BingX: отримано {len(bingx)} монет")
    except Exception:
        logging.exception("❌ Помилка при отриманні цін з BingX")

    if not any([bitget, kucoin, okx, mexc, bingx]):
        logging.warning("⚠️ Жодна біржа не повернула дані — припиняю пошук арбітражу")
        return []

    exchanges = {
        "Bitget": bitget,
        "Kucoin": kucoin,
        "OKX": okx,
        "MEXC": mexc,
        "BingX": bingx
    }

    # Знаходимо спільні монети
    common_coins = set.intersection(*[set(prices.keys()) for prices in exchanges.values()])
    logging.info(f"🔎 Знайдено {len(common_coins)} спільних монет")

    opportunities = []

    for coin in common_coins:
        coin_prices = {name: data.get(coin) for name, data in exchanges.items()}

        for buy_exchange, buy_data in coin_prices.items():
            if not buy_data:
                continue

            buy_price = buy_data.get("ask")
            volume = buy_data.get("volume", 0)
            if not buy_price or buy_price > PRICE_LIMIT or volume < VOLUME_LIMIT:
                continue

            for sell_exchange, sell_data in coin_prices.items():
                if not sell_data or sell_exchange == buy_exchange:
                    continue

                sell_price = sell_data.get("bid")
                if not sell_price or sell_price < buy_price:
                    continue

                profit_percent = (sell_price - buy_price) / buy_price * 100

                if profit_percent >= PROFIT_THRESHOLD:
                    opportunity = {
                        "coin": coin,
                        "buy_from": buy_exchange,
                        "sell_to": sell_exchange,
                        "buy_price": round(buy_price, 6),
                        "sell_price": round(sell_price, 6),
                        "profit_percent": round(profit_percent, 2)
                    }
                    opportunities.append(opportunity)

    return sorted(opportunities, key=lambda x: x["profit_percent"], reverse=True)

