async def get_kucoin_prices():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"KuCoin API error {resp.status}: {await resp.text()}")
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["last"]),
                    "volume": float(item["vol"])
                }
                for item in data["data"]["ticker"]
                if item["symbol"].endswith("USDT")
            }
