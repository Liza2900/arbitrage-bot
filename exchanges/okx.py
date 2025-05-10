async def get_okx_prices():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"OKX API error {resp.status}: {await resp.text()}")
            data = await resp.json()
            return {
                item["instId"]: {
                    "price": float(item["last"]),
                    "volume": float(item["volCcy24h"])
                }
                for item in data["data"]
                if item["instId"].endswith("USDT")
            }
