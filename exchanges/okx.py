import aiohttp

async def get_okx_prices():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        async with session.get(url) as resp:
            data = await resp.json()
            result = {}

            for item in data["data"]:
                symbol = item["instId"]
                if not symbol.endswith("USDT"):
                    continue

                try:
                    price = float(item["last"])
                    volume = float(item["volCcyQuote"])
                except (KeyError, ValueError):
                    continue

                result[symbol] = {
                    "price": price,
                    "volume": volume
                }

            return result
