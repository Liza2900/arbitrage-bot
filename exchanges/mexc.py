import aiohttp

BASE_URL = "https://api.mexc.com"

async def get_orderbook_mexc(symbol: str) -> dict:
    """Повертає ціну, бид, аск і фейковий обсяг для символу USDT"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/v3/ticker/bookTicker") as resp:
            data = await resp.json()

    for item in data:
        if item["symbol"] == symbol.replace("-", ""):  # Наприклад: BTC-USDT → BTCUSDT
            price = (float(item["bidPrice"]) + float(item["askPrice"])) / 2
            return {
                "price": price,
                "bid": float(item["bidPrice"]),
                "ask": float(item["askPrice"]),
                "volume": 99999  # MEXC не дає обсягів
            }
    return None

async def get_tradable_symbols_mexc() -> list:
    """Повертає список доступних символів USDT"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/v3/ticker/bookTicker") as resp:
            data = await resp.json()

    symbols = []
    for item in data:
        if item["symbol"].endswith("USDT"):
            # BTCUSDT → BTC-USDT
            formatted = item["symbol"].replace("USDT", "") + "-USDT"
            symbols.append(formatted)
    return symbols
