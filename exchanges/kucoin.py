import aiohttp

async def get_kucoin_prices():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {item["symbol"]: float(item["last"]) for item in data["data"]["ticker"]}