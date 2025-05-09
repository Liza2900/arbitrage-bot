import aiohttp

async def get_bybit_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            result = {}

            for item in data["result"]["list"]:
                symbol = item["symbol"]
                if not symbol.endswith("USDT"):
                    continue  # Пропускаємо не-USDT пари

                try:
                    price = float(item["lastPrice"])
                    volume = float(item["quoteVolume24h"])
                except (KeyError, ValueError):
                    continue  # Пропускаємо зламані пари

                result[symbol] = {
                    "price": price,
                    "volume": volume
                }

            return result
