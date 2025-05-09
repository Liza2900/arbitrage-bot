import aiohttp

async def get_bitget_prices():
    url = "https://api.bitget.com/api/spot/v1/market/tickers"
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            result = {}

            for item in data["data"]:
                symbol = item["symbol"]
                if not symbol.endswith("USDT"):
                    continue  # Пропускаємо не-USDT пари

                try:
                    price = float(item["lastPr"])
                    volume = float(item["quoteVol"])
                except (KeyError, ValueError):
                    continue

                result[symbol] = {
                    "price": price,
                    "volume": volume
                }

            return result
