async def get_bitget_prices():
    url = "https://api.bitget.com/api/spot/v1/market/tickers"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Bitget API error {resp.status}: {await resp.text()}")
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["lastPr"]),
                    "volume": float(item["baseVol"])
                }
                for item in data["data"]
                if item["symbol"].endswith("USDT")
            }
