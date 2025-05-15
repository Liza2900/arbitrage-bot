import aiohttp

BASE_URL = "https://api.mexc.com"

async def get_mexc_prices():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/v3/ticker/bookTicker") as resp:
            data = await resp.json()

    result = {}
    for item in data:
        symbol = item["symbol"]
        bid = item.get("bidPrice")
        ask = item.get("askPrice")

        # Пропускаємо, якщо ціни відсутні
        if symbol.endswith("USDT") and bid and ask:
            try:
                price = (float(bid) + float(ask)) / 2
                result[symbol.replace("USDT", "")] = {
                    "price": price,
                    "bid": float(bid),
                    "ask": float(ask),
                    "volume": 99999  # MEXC не дає обсягів
                }
            except ValueError:
                continue  # Пропустити, якщо конвертація в float не вдалась

    return result
