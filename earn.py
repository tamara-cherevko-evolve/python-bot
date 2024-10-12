from decimal import Decimal
from ballance import get_balance_usdt
from constants import minimum_earn_balance 
from binance.client import Client 
from create_order import get_price_btcusd
from db import get_all_earn_data

def select_coin_for_suggestion(): 

    all_data = get_all_earn_data()
    # Find the coin with the lowest earnings total
    lowest_earning_coin = min(all_data.items(), key=lambda x: Decimal(x[1]['diff_in_percent']))
 
    return lowest_earning_coin[0] 


 
def buy_coin(client, coin): 
    symbol = f"{coin}USDT"
    price_info = client.get_symbol_ticker(symbol=symbol)
    price = float(price_info['price'])
        
    # Calculate the amount of the coin that can be bought
    amount = round(Decimal(minimum_earn_balance) / Decimal(price), 2)
    print(f"Amount of {coin} that can be bought for ${minimum_earn_balance}: {amount:.8f}")
    return amount
    # order = client.create_order(
    #     symbol=symbol,
    #     side=Client.SIDE_BUY,
    #     type=Client.ORDER_TYPE_MARKET,
    #     quantity=amount
    # )

    # return order

def check_balance_for_earn_investment(client):
    balance = get_balance_usdt(client) 
    is_balance_enough = balance >= minimum_earn_balance
    message = ''

    if balance >= minimum_earn_balance:
        message = f"Sufficient balance: ${balance:.2f}" 
    else:
        message = f"Insufficient balance: ${balance:.2f}, Minimum balance: ${minimum_earn_balance:.2f}" 
    
    summary_data = {
        "is_balance_enough": is_balance_enough,
        "message": message, 
    }
    return summary_data

# Example usage
if __name__ == "__main__":
    suggested_coin = select_coin_for_suggestion()
    print(f"Suggested coin for buy: {suggested_coin}")


