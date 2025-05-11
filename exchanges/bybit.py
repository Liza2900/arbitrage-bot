import aiohttp

BYBIT_URL = "https://api.bybit.com/v5/market/tickers?category=spot"

async def get_bybit_prices():
    headers = {
        "User-Agent": "Mozilla/5.0"  # важливо для уникнення помилок 403
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BYBIT_URL) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Bybit API error {resp.status}: {text}")
            data = await resp.json()

    prices = {}
    for item in data["result"]["list"]:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            price = float(item["lastPrice"])
            volume = float(item["turnover24h"])
            prices[symbol] = {"price": price, "volume": volume}
    return prices

