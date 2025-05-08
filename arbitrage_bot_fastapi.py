from fastapi import FastAPI
from arbitrage import find_arbitrage_opportunities

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Arbitrage Bot is running."}

@app.get("/arbitrage")
async def get_arbitrage():
    return await find_arbitrage_opportunities()