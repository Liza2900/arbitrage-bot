import aiohttp

async def get_bybit_prices():
    url = "https://api.bybit.com/v5/market/tickers?category=spot"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return {item["symbol"]: float(item["lastPrice"]) for item in data["result"]["list"]}