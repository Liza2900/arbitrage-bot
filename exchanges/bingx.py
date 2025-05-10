import aiohttp

async def get_bingx_prices():
    url = "https://api-swap-rest.bingx.com/api/v1/market/getAllContracts"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {
                item["symbol"]: {
                    "price": float(item["lastPrice"]),
                    "volume": float(item["volume24h"])
                }
                for item in data["data"]
                if item["symbol"].endswith("USDT")
            }
