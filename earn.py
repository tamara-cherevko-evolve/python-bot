from decimal import Decimal
from ballance import get_balance_usdt
from constants import minimum_earn_balance, Coin
from db import get_all_earn_data

def select_coin_for_suggestion(): 

    all_data = get_all_earn_data()
    # Find the coin with the lowest earnings total
    lowest_earning_coin = min(all_data.items(), key=lambda x: Decimal(x[1]['diff_in_percent']))
 
    return lowest_earning_coin[0] 
 
# def buy_coin(client, coin):
#     # Check if balance is sufficient
#     price = get_balance_usdt(client)
#     minimum_balance = get_minimum_balance(price)
#     is_balance_enough = check_balance_for_orders(client, price)
#     if not is_balance_enough:
#         return

def check_balance_for_orders(client):
    balance = get_balance_usdt(client) 

    if balance >= minimum_earn_balance:
        print(f"Sufficient balance: {balance}")
        return True
    else:
        print(f"Insufficient balance: {balance}, minimum balance: {minimum_earn_balance}")
        return False
# Example usage
if __name__ == "__main__":
    suggested_coin = select_coin_for_suggestion()
    print(f"Suggested coin for buy: {suggested_coin}")


