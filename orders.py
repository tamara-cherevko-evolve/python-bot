from datetime import datetime
import json
from calculation import calculate_avg_price, calculate_expected_profit, calculate_nex_DCA_price, calculate_take_profit_price, calculate_total_quantity, calculate_total_spent
from constants import *
from time import sleep 
from binance.client import Client 

from create_order import start_DCA_grid
from file_utils import add_data_to_json_file, clean_file, get_buy_orders_ids_from_file, get_completed_orders_from_file, get_orders_to_listen_from_file, get_sell_order_id_from_file, update_buy_ids_in_json, update_sell_id_in_json 

def delete_all_orders(client):
    try:
        open_orders = client.get_open_orders(symbol=current_symbol) 

        for order in open_orders:
            try: 
                client.cancel_order(orderId=order['orderId'], symbol=current_symbol)    
                print(f"Order {order['orderId']} has been canceled")
            except Exception as e:
                print(f"Failed to cancel order {order['orderId']}:", e)
        print("All orders have been canceled")
    except Exception as e:
        print("Failed to cancel orders:", e)

def delete_order_by_id(client, order_id):
    try: 
        client.cancel_order(orderId=order_id, symbol=current_symbol)    
        print(f"Order {order_id} has been canceled")
    except Exception as e:
        print(f"Failed to cancel order {order_id}:", e)

def start_listening_orders(client):
    all_orders_details = [] 
 
    dca_orders_ids = get_orders_to_listen_from_file(file_listening_orders) 
     
    if len(dca_orders_ids) <= 0:
        return []
    
    for id in dca_orders_ids:
        order_check = client.get_order(symbol=current_symbol, orderId=id)
        order_status = order_check['status']
        order_side = order_check['side']
        all_orders_details.append(order_check) 

        if order_status == "FILLED":
            if order_side == "SELL":
                delete_all_orders(client)
                clean_file(file_orders_in_progress)
                clean_file(file_listening_orders)
                print("Sell Order Filled And New DCA Grid Started")
                start_DCA_grid(client)
            elif order_side == "BUY":
                # Delete filled BUY order from listening orders
                buy_order_ids = get_buy_orders_ids_from_file(file_listening_orders)
                filtered_buy_order_ids = [order_id for order_id in buy_order_ids if order_id != order_check['orderId']] 
                update_buy_ids_in_json(file_listening_orders, filtered_buy_order_ids)

                # Delete previous sell order
                sell_order = get_sell_order_id_from_file(file_listening_orders)
                delete_order_by_id(client, sell_order)

                # Move the completed buy order to the file with completed orders
                completed_orders_from_file = get_completed_orders_from_file(file_orders_in_progress)
                completed_buy_orders = [*completed_orders_from_file, order_check]
                add_data_to_json_file(file_orders_in_progress, completed_buy_orders, 'completed_orders')  

                # Calculate the average price 
                average_price = calculate_avg_price(completed_buy_orders)

                # Create new take profit order
                total_quantity = calculate_total_quantity(completed_buy_orders)
                tp_price = calculate_take_profit_price(average_price, total_quantity)
                tp_order = client.create_order(symbol=current_symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity=total_quantity, timeInForce='GTC', price=tp_price) 
                tp_order_id = tp_order['orderId'] 
                update_sell_id_in_json(file_listening_orders, tp_order_id)
                print("Buy Order Filled")  

    btcusd_price = client.get_symbol_ticker(symbol=current_symbol)   
    current_price = btcusd_price['price']

    last_update = datetime.now()
    last_update_str = last_update.strftime('%Y-%m-%d %H:%M:%S') 

    completed_orders_from_file = get_completed_orders_from_file(file_orders_in_progress)
    average_price = calculate_avg_price(completed_orders_from_file) 
    total_quantity = calculate_total_quantity(completed_orders_from_file)
    tp_price = calculate_take_profit_price(average_price, total_quantity)
    expected_profit = calculate_expected_profit(completed_orders_from_file)
    total_spent = calculate_total_spent(completed_orders_from_file)

    print("Last update:", last_update_str)
    
    return  {
        "orders_are_listening": all_orders_details,
        "current_price": current_price,
        "last_update": last_update_str,
        "completed_orders": completed_orders_from_file,
        "average_price": average_price,
        "total_quantity": total_quantity,
        "tp_price": tp_price,
        "expected_profit": expected_profit,
        "total_spent": total_spent
    } 

def recalculate_sell_order(client):
    try:
        completed_orders_from_file = get_completed_orders_from_file(file_orders_in_progress)  
        average_price = calculate_avg_price(completed_orders_from_file)
        total_quantity = calculate_total_quantity(completed_orders_from_file)
        tp_price = calculate_take_profit_price(average_price, total_quantity)
        print(total_quantity)
        tp_order = client.create_order(symbol=current_symbol, side=Client.SIDE_SELL, type=Client.ORDER_TYPE_LIMIT, quantity=total_quantity, timeInForce='GTC', price=tp_price) 
        tp_order_id = tp_order['orderId'] 
        update_sell_id_in_json(file_listening_orders, tp_order_id)
        print("Buy Order Filled") 
    
    except Exception as e:
        print(f"An error occurred: {e}")