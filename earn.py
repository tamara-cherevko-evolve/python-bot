from datetime import datetime
from decimal import Decimal
from ballance import get_balance_usdt
from constants import minimum_earn_balance 
from binance.client import Client  
from db import get_all_earn_data, insert_coin_purchase

def select_coin_for_suggestion(): 

    all_data = get_all_earn_data()
    # Find the coin with the lowest earnings total
    lowest_earning_coin = min(all_data.items(), key=lambda x: Decimal(x[1]['diff_in_percent']))
 
    return lowest_earning_coin[0] 


 
def buy_coin(client, coin): 
    try:
        symbol = f"{coin}USDT"
        price_info = client.get_symbol_ticker(symbol=symbol)
        price = float(price_info['price'])
            
        # Calculate the amount of the coin that can be bought
        amount = round(Decimal(minimum_earn_balance) / Decimal(price), 5) 
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=amount
        )

        if order and 'orderId' in order:
            # Add order data to the database
            transact_time = datetime.fromtimestamp(order['transactTime'] / 1000).strftime('%Y-%m-%d')
            qty = float(order['executedQty'])
            price = float(order['price'])
            # Extract the commission from the order
            commission_rate = sum(float(fill['commission']) for fill in order['fills'])
            commission = float(price) * commission_rate
            total = float(order['cummulativeQuoteQty'])  
            insert_coin_purchase(coin, transact_time, qty, price, total, commission)
            
            return order
    except Exception as e:
        return {"status": "error", "message": str(e)}

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


