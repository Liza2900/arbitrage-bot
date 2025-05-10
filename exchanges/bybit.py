import aiohttp

async def get_bybit_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["lastPrice"]),
                    "volume": float(item["quoteVolume24h"])
                }
                for item in data["result"]["list"]
                if item["symbol"].endswith("USDT")
            }
