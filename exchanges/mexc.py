import aiohttp

BASE_URL = "https://api.mexc.com"

async def get_mexc_prices():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/v3/ticker/bookTicker") as resp:
            data = await resp.json()

    result = {}
    for item in data:
        symbol = item["symbol"]
        if symbol.endswith("USDT"):
            price = (float(item["bidPrice"]) + float(item["askPrice"])) / 2
            result[symbol.replace("USDT", "")] = {
                "price": price,
                "bid": float(item["bidPrice"]),
                "ask": float(item["askPrice"]),
                "volume": 99999  # MEXC не дає обсягів у цьому ендпоінті
            }
    return result
