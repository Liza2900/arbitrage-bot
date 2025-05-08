import aiohttp

async def get_bitget_prices():
    url = "https://api.bitget.com/api/spot/v1/market/tickers"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {item["symbol"]: float(item["lastPr"]) for item in data["data"]}