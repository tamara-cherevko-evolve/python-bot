import os
from dotenv import load_dotenv 
from decimal import Decimal
from binance.client import Client 
from constants import Coin
from binance.client import Client 

load_dotenv()
client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET")) 

def get_current_price(symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol) 
        return Decimal(ticker['price'])
    except Exception as e:
        print(f"Error fetching current price for {symbol}: {e}")
        return Decimal(0)