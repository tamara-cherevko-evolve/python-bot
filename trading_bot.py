from datetime import time
from binance.client import Client
import pandas as pd
import numpy as np
from time import sleep
from binance.exceptions import BinanceAPIException, BinanceOrderException
import math 
from calculation import calculate_take_profit_price
from constants import *
from create_order import start_DCA_grid
from file_utils import get_completed_orders_from_file, get_orders_to_listen_from_file, update_sell_id_in_json, write_orders_to_listen
from orders import delete_all_orders, start_listening_orders

client = Client(api_key, api_secret)  

# start_DCA_grid(client)

# delete_all_orders(client)  
 
# ids = get_orders_to_listen_from_file(file_listening_orders)
# try:
#     open_orders = client.get_open_orders()
#     for order in open_orders:
#         print(order)

# except BinanceAPIException as e:
#     print(f"Binance API Exception occurred: {e}")
# except BinanceOrderException as e:
#     print(f"Binance Order Exception occurred: {e}")

# start_listening_orders(client)

  # Calculate the average price

