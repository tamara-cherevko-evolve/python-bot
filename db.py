from enum import Enum
import json
import mysql.connector
from mysql.connector import Error

from binance.exceptions import BinanceAPIException, BinanceOrderException
from constants import *
from dotenv import load_dotenv
import os
from datetime import date, datetime
from decimal import Decimal

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

class Coin(Enum):
    BTC = 'BTC'
    ADA = 'ADA'
    ETH = 'ETH'
    PEPE = 'PEPE'
    SOL = 'SOL'

def get_BTC_earn_data():
    return get_earn_data(Coin.BTC)

def get_ADA_earn_data():
    return get_earn_data(Coin.ADA)

def get_ETH_earn_data():
    return get_earn_data(Coin.ETH)

def get_PEPE_earn_data():
    return get_earn_data(Coin.PEPE)

def get_SOL_earn_data():
    return get_earn_data(Coin.SOL)

def get_earn_data(coin: Coin):
    return get_earn_data_from_db(f"{coin.value}_Earn")

def get_earn_data_from_db(table_name):
    connection = None
    print(db_config)
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
                        item[key] = str(value)
                items.append(item)
 
            # Close the cursor
            cursor.close() 
            # Return the data as JSON
            return json.dumps(items)
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    get_BTC_earn_data()