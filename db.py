 
import mysql.connector
from mysql.connector import Error
from binance.client import Client 
 
from constants import Coin
from dotenv import load_dotenv
import os
from datetime import date, datetime
from decimal import Decimal

from price import get_current_price

# Load environment variables from .env file
load_dotenv()

# MySQL connection configuration using environment variables
db_config = {
    'host': os.getenv('DB_HOSTNAME'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD')
} 

client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET")) 

def insert_coin_purchase(coin, date, amount, price, total, commission): 
    try:
        connection = mysql.connector.connect(**db_config)
        if connection and connection.is_connected(): 
            cursor = connection.cursor()
            table_name = f"{coin}_Earn" 
            cursor.execute(f"INSERT INTO {table_name} (date, amount, price, total, commission) VALUES ('{date}', {amount}, {price}, {total}, {commission})")
            connection.commit() 
            connection.close()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def get_earn_data(coin):
    return get_earn_data_from_db(f"{coin}_Earn")

def get_all_earn_data():
    all_data = {
        Coin.BTC.value: get_earn_summary(Coin.BTC.value),
        Coin.ADA.value: get_earn_summary(Coin.ADA.value),
        Coin.ETH.value: get_earn_summary(Coin.ETH.value),
        Coin.PEPE.value: get_earn_summary(Coin.PEPE.value),
        Coin.SOL.value: get_earn_summary(Coin.SOL.value)
    }
 
    return all_data

def get_earn_summary(coin):
    items = get_earn_data(coin) 
    summary_data = {
        "coin": coin,
        "amount": 0,
        "spent": 0,
        "diff_in_dollars": 0,
        "diff_in_percent": 0,
        "current_price": 0,
        "avg_price": 0
    }

    # Calculate total amount
    total_amount = sum(Decimal(item["amount"] or 0) for item in items)
    total_spent = sum(Decimal(item["total"] or 0) for item in items)
    current_price = get_current_price(f"{coin}USDT") 
    total_current_value = current_price * total_amount
    
    if total_amount > 0:
        avg_price = total_spent / total_amount
        diff_in_dollars = total_current_value - total_spent
        diff_in_percent = (diff_in_dollars / total_spent) * 100 if total_spent > 0 else 0
        summary_data["coin"] = f"{coin}"
        summary_data["amount"] = f"{total_amount:.8f}"
        summary_data["spent"] = f"{total_spent:.8f}"
        summary_data["diff_in_dollars"] = f"{diff_in_dollars:.8f}"
        summary_data["diff_in_percent"] = f"{diff_in_percent:.2f}"
        summary_data["current_price"] = f"{current_price:.8f}"
        summary_data["avg_price"] = f"{avg_price:.8f}"
    
    return summary_data 

def get_earn_data_from_db(table_name):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        if connection and connection.is_connected(): 
            cursor = connection.cursor()
            
            # Execute a query to fetch data from BTC_Earn table
            cursor.execute(f"SELECT * FROM {table_name}") 
            
            # Fetch all rows from the executed query
            rows = cursor.fetchall()
            
             # Fetch column names
            column_names = [i[0] for i in cursor.description]
            
            # Convert rows to a list of dictionaries
            items = []
            for row in rows:
                item = {column_names[i]: row[i] for i in range(len(column_names))}
                # Convert date and Decimal objects to string
                for key, value in item.items():
                    if isinstance(value, (date, datetime)):
                        item[key] = value.isoformat()
                    elif isinstance(value, Decimal):
                        item[key] = f"{value:.8f}"
                items.append(item)
 
            # Sort items by date in descending order
            items = sorted(items, key=lambda x: x['date'], reverse=True)

            # Close the cursor 
            cursor.close() 
            # Return the data as JSON
            return items
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__": 
    info = client.get_symbol_info('ETHUSDT')
    print(info)