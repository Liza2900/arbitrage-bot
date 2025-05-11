import logging

async def find_arbitrage_opportunities():
    try:
        bitget = await get_bitget_prices()
        kucoin = await get_kucoin_prices()
        okx = await get_okx_prices()
        bybit = await get_bybit_prices()
        bingx = await get_bingx_prices()
        logging.info("Ціни успішно отримано з усіх бірж")

        # тут можна вивести кількість монет з кожної
        logging.info(f"Bitget: {len(bitget)}, Kucoin: {len(kucoin)}, OKX: {len(okx)}, Bybit: {len(bybit)}, BingX: {len(bingx)}")

        # основна логіка
        ...

        return opportunities  # список словників

    except Exception as e:
        logging.exception("Помилка при пошуку арбітражу")
        return []
