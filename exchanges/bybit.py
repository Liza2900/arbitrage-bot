import aiohttp

async def get_bybit_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"Bybit API error {resp.status}: {text}")
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["lastPrice"]),
                    "volume": float(item["turnover24h"])
                }
                for item in data["result"]["list"]
                if item["symbol"].endswith("USDT")
            }
