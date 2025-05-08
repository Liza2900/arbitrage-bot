from exchanges.bybit import get_bybit_prices
from exchanges.kucoin import get_kucoin_prices
from exchanges.bitget import get_bitget_prices
from exchanges.okx import get_okx_prices
from exchanges.bingx import get_bingx_prices

async def find_arbitrage_opportunities():
    bybit = await get_bybit_prices()
    kucoin = await get_kucoin_prices()
    bitget = await get_bitget_prices()
    okx = await get_okx_prices()
    bingx = await get_bingx_prices()

    return {
        "bybit": list(bybit.items())[:5],
        "kucoin": list(kucoin.items())[:5],
        "bitget": list(bitget.items())[:5],
        "okx": list(okx.items())[:5],
        "bingx": list(bingx.items())[:5],
    }