import json
from datetime import datetime
from binance.client import Client
import os
from calculation import calculate_take_profit_price
from constants import *

def write_status_to_file(filename, status):  
    
    # Write the updated data back to the file
    with open(filename, 'w') as file: 
        json.dump({'connection':  status.value}, file, indent=4)
        
    print(f"Connection status have been written to {filename}")

def write_orders_to_listen(filename, ids):  
    
    # Write the updated data back to the file
    with open(filename, 'w') as file: 
        json.dump(ids, file, indent=4)
        
    print(f"Orders to listen have been written to {filename}")

def get_orders_to_listen_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            buy_ids = data.get('buy_ids', [])
            sell_id = data.get('sell_id')
 
            return [*buy_ids, sell_id]
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        return []
    
def get_buy_orders_ids_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('buy_ids', [])
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        return []
    
def get_sell_order_id_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('sell_id')
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        return []
    
def update_sell_id_in_json(file_path, new_sell_id):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        data['sell_id'] = new_sell_id  # Update the sell_id
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"Updated sell_id to {new_sell_id}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")

def update_buy_ids_in_json(file_path, new_buy_ids):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        data['buy_ids'] = new_buy_ids 
        with open(file_path, 'w') as file:
            json.dump(data, file)
        print(f"Updated buy_ids to {new_buy_ids}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
    
def clean_file(filename): 
    try:
        # Open the file in write mode to truncate it to zero length
        with open(filename, 'w'):
            pass  # Opening in 'w' mode and closing it will clear the file
        print(f"{filename} has been cleared.")
    except Exception as e:
        print(f"An error occurred while clearing the file: {e}") 

def add_data_to_json_file(filename, new_data, name): 
    # Initialize or load the JSON structure
    data_structure = {}
    
    # Check if the file exists and is not empty
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        # Read the existing data
        with open(filename, 'r') as file:
            data_structure = json.load(file)  
            
    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump({**data_structure, name: new_data}, file, indent=4) 

def get_completed_orders_from_file(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('completed_orders', [])
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        return []



def write_order_details(filename, order):
    try:
        # Extract order details
        transact_time = order['transactTime']
        qty = order['executedQty']
        price = order['price'] 
        # Extract the commission from the order
        commission_rate = sum(float(fill['commission']) for fill in order['fills'])
        commission = float(price) * commission_rate
        total = order['cummulativeQuoteQty'] 

        # Convert timestamp to readable date
        date_of_placing_buy_order = datetime.fromtimestamp(transact_time / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Prepare data to write
        order_details = { 
            'order_id': order['orderId'],
            'dateOfPlacingBuyOrder': date_of_placing_buy_order,
            'qty': qty,
            'price': price,
            'commission': commission,
            'total': total 
        }

        # Write the order details to a file
        add_data_to_json_file(filename, [order_details], 'completed_orders')
    
    except Exception as e:
        print(f"An error occurred: {e}")

