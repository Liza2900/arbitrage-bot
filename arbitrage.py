from exchanges.mexc import get_mexc_prices
from exchanges.kucoin import get_kucoin_prices
from exchanges.bitget import get_bitget_prices
from exchanges.okx import get_okx_prices
from exchanges.bingx import get_bingx_prices

PRICE_LIMIT = 15
VOLUME_LIMIT = 10

async def find_arbitrage_opportunities():
    # Отримуємо дані
    mexc = await get_mexc_prices()
    kucoin = await get_kucoin_prices()
    bitget = await get_bitget_prices()
    okx = await get_okx_prices()
    bingx = await get_bingx_prices()

    exchanges = {
        "mexc": mexc,
        "kucoin": kucoin,
        "bitget": bitget,
        "okx": okx,
        "bingx": bingx,
    }

    # Збір унікальних символів
    all_symbols = set()
    for data in exchanges.values():
        all_symbols.update(data.keys())

    opportunities = []

    for symbol in all_symbols:
        prices = []
        for name, data in exchanges.items():
            if symbol in data:
                info = data[symbol]
                price = info["price"]
                volume = info["volume"]
                if price <= PRICE_LIMIT and volume >= VOLUME_LIMIT:
                    prices.append((name, price))

        if len(prices) < 2:
            continue

        # Знаходимо максимальну і мінімальну ціну
        prices.sort(key=lambda x: x[1])
        min_exchange, min_price = prices[0]
        max_exchange, max_price = prices[-1]

        spread_percent = ((max_price - min_price) / min_price) * 100

        if spread_percent >= 0.8:
            opportunities.append({
                "symbol": symbol,
                "buy": {"exchange": min_exchange, "price": min_price},
                "sell": {"exchange": max_exchange, "price": max_price},
                "spread_percent": round(spread_percent, 2)
            })

    return opportunities
