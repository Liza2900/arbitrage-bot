import aiohttp  # ← Додай це
import json

BASE_URL = "https://api.kucoin.com"

async def get_kucoin_prices():
    headers = {
        "Accept": "application/json"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"{BASE_URL}/api/v1/market/allTickers") as resp:
            data = await resp.json()

    result = {}
    for ticker in data["data"]["ticker"]:
        symbol = ticker["symbol"]
        if symbol.endswith("-USDT"):
            try:
                price = float(ticker["last"])
                vol = float(ticker["vol"])
                result[symbol] = {
                    "price": price,
                    "volume": vol
                }
            except (ValueError, TypeError):
                continue

    return result
