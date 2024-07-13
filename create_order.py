from datetime import time
from binance.client import Client 
from time import sleep
from binance.exceptions import BinanceAPIException 
from ballance import check_balance_for_orders 
from calculation import calculate_nex_DCA_price, calculate_take_profit_price
from constants import *
from file_utils import add_data_to_json_file, write_order_details, clean_file, write_orders_to_listen
# from orders import delete_all_orders, start_listening_orders   

# Open new order with the last price, and set TP and SL:
def start_DCA_grid(client):  
    price_info = client.get_symbol_ticker(symbol=current_symbol)
    price = float(price_info['price'])
    buy_order_ids = [] 

    # Check if the balance is sufficient for the orders
    if_ballance_enough = check_balance_for_orders(client, price)
    if not if_ballance_enough:
        error_message = {"error": "Insufficient balance"}
        return error_message 

    try:
        # Buy first share
        first_share = client.create_order(symbol=current_symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=buy_qty)
        print(current_symbol, 'BUY', f"placing order, price: {price}") 
        add_data_to_json_file(file_orders_in_progress, [first_share], 'completed_orders') 
        sleep(2)

        # Create DCA orders
        for i in range(int(risk_buy_more_times)):
            sl_price = calculate_nex_DCA_price(price, i+1) 
            dca_order = client.create_order(symbol=current_symbol, side=Client.SIDE_BUY, type=Client.ORDER_TYPE_LIMIT, quantity=buy_qty, timeInForce='GTC', price=sl_price)
            buy_order_ids.append(dca_order['orderId'])
            print(f"DCA order {i}: {sl_price}")  
            sleep(2) 
        
        # Create TP orders
        tp_price = calculate_take_profit_price(price, buy_qty)
        tp_order = client.create_order(symbol=current_symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity=buy_qty, timeInForce='GTC', price=tp_price) 
        sell_order_id = tp_order['orderId']
        data_to_write = {
            "buy_ids": buy_order_ids,
            "sell_id": sell_order_id
        }
        print(f"Take Profit Order: {tp_price}") 
        write_orders_to_listen(file_listening_orders, data_to_write)  
        return data_to_write

    except BinanceAPIException as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.message
            )
        ) 
        