async def get_bingx_prices():
    url = "https://api-swap-rest.bingx.com/api/v1/market/getAllContracts"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"BingX API error {resp.status}: {await resp.text()}")
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["lastPrice"]),
                    "volume": float(item["volume24h"])
                }
                for item in data["data"]
                if item["symbol"].endswith("USDT")
            }
