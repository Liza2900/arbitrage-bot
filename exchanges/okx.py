import aiohttp

async def get_okx_prices():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {item["instId"]: float(item["last"]) for item in data["data"]}