from exchanges.bybit import get_bybit_prices
from exchanges.kucoin import get_kucoin_prices
from exchanges.bitget import get_bitget_prices
from exchanges.okx import get_okx_prices
from exchanges.bingx import get_bingx_prices

async def find_arbitrage_opportunities():
    exchanges = {
        "bybit": await get_bybit_prices(),
        "kucoin": await get_kucoin_prices(),
        "bitget": await get_bitget_prices(),
        "okx": await get_okx_prices(),
        "bingx": await get_bingx_prices(),
    }

    results = []

    exchange_names = list(exchanges.keys())

    for symbol in set().union(*[set(data.keys()) for data in exchanges.values()]):
        prices = []
        for name in exchange_names:
            data = exchanges[name].get(symbol)
            if data and data["price"] < 15 and data["volume"] >= 10:
                prices.append({
                    "exchange": name,
                    "price": data["price"],
                    "volume": data["volume"]
                })

        for buy in prices:
            for sell in prices:
                if buy["exchange"] != sell["exchange"]:
                    profit_pct = (sell["price"] - buy["price"]) / buy["price"] * 100
                    if profit_pct >= 0.8:
                        results.append({
                            "symbol": symbol,
                            "buy_exchange": buy["exchange"],
                            "sell_exchange": sell["exchange"],
                            "buy_price": buy["price"],
                            "sell_price": sell["price"],
                            "profit_percent": round(profit_pct, 2)
                        })

    return results
