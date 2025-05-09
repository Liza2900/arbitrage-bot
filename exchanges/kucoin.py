import aiohttp

async def get_kucoin_prices():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            result = {}

            for item in data["data"]["ticker"]:
                symbol = item["symbol"]
                if not symbol.endswith("USDT"):
                    continue

                try:
                    price = float(item["last"])
                    volume = float(item["volValue"])  # обсяг в quote (USDT)
                except (KeyError, ValueError):
                    continue

                result[symbol] = {
                    "price": price,
                    "volume": volume
                }

            return result
