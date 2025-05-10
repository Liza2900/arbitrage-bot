async def find_arbitrage_opportunities():
    from exchanges.bybit import get_bybit_prices
    from exchanges.kucoin import get_kucoin_prices
    from exchanges.bitget import get_bitget_prices
    from exchanges.okx import get_okx_prices
    from exchanges.bingx import get_bingx_prices

    exchanges = {
        "bybit": await get_bybit_prices(),
        "kucoin": await get_kucoin_prices(),
        "bitget": await get_bitget_prices(),
        "okx": await get_okx_prices(),
        "bingx": await get_bingx_prices(),
    }

    opportunities = []
    symbols = set()
    for data in exchanges.values():
        symbols.update(data.keys())

    for symbol in symbols:
        prices = []
        for name, data in exchanges.items():
            if symbol in data:
                price = data[symbol]["price"]
                volume = data[symbol]["volume"]
                if price < 15 and volume > 10:
                    prices.append((name, price))

        if len(prices) < 2:
            continue

        prices.sort(key=lambda x: x[1])
        min_ex, min_price = prices[0]
        max_ex, max_price = prices[-1]

        spread_percent = ((max_price - min_price) / min_price) * 100

        if spread_percent >= 0.8:
            opportunities.append({
                "symbol": symbol,
                "buy_from": min_ex,
                "buy_price": round(min_price, 4),
                "sell_on": max_ex,
                "sell_price": round(max_price, 4),
                "spread": round(spread_percent, 2)
            })

    return opportunities
