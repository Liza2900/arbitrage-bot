import aiohttp

async def get_bingx_prices():
    url = "https://api-swap-rest.bingx.com/api/v1/market/getAllContracts"
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            result = {}

            for item in data["data"]:
                symbol = item["symbol"]
                if not symbol.endswith("USDT"):
                    continue  # Пропускаємо не-USDT пари

                try:
                    price = float(item["lastPrice"])
                    volume = float(item["quoteVolume"])
                except (KeyError, ValueError):
                    continue

                result[symbol] = {
                    "price": price,
                    "volume": volume
                }

            return result
