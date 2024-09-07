from binance.exceptions import BinanceAPIException, BinanceOrderException
from constants import *

# getting your spot balance in USDT
def get_balance_usdt(client):
    try:
        account_details = client.get_account()
        balances = account_details['balances']
        for balance in balances:
            if balance['asset'] == 'USDT':
                free_ballance = float(balance['free']) # 'free' represents the available balance
                print(f"USDT Balance: {free_ballance}")
                return free_ballance  
   

    except BinanceAPIException as error:
        print(
            "Found error. status: {}, error code: {}, error message: {}".format(
                error.status_code, error.code, error.message
            )
        )

def get_minimum_balance(price):  
    # Calculate the total cost for orders without placing them
    total_cost = price * buy_qty * risk_buy_more_times  
    return total_cost 
    
def check_balance_for_orders(client, price):
    balance = get_balance_usdt(client)   
    minimum_balance = get_minimum_balance(price)
        
    if balance >= minimum_balance:
        print(f"Sufficient balance. Total cost for 20 orders: {minimum_balance}, Available balance: {balance}")
        return True
    else:
        print(f"Insufficient balance. Total cost for 20 orders: {minimum_balance}, Available balance: {balance}")  
        return False