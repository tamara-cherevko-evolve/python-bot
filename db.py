 
import mysql.connector
from mysql.connector import Error
 
from constants import Coin
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

def get_earn_data(coin):
    return get_earn_data_from_db(f"{coin}_Earn")

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
    get_earn_data(Coin.BTC.value)