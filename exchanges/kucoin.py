import aiohttp

async def get_kucoin_prices():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["last"]),
                    "volume": float(item["volValue"])  # USDT обсяг
                }
                for item in data["data"]["ticker"]
                if item["symbol"].endswith("USDT")
            }
