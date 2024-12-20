import calendar
from datetime import datetime
from decimal import Decimal
from ballance import get_balance_usdt
from constants import minimum_earn_balance, coins_round_to, earn_start_date 
from binance.client import Client  
from db import get_all_earn_data, insert_coin_purchase

def select_coin_for_suggestion(): 

    all_data = get_all_earn_data()
    # Find the coin with the lowest earnings total
    lowest_earning_coin = min(all_data.items(), key=lambda x: Decimal(x[1]['diff_in_percent']))
 
    return lowest_earning_coin[0] 


def select_purchase_amount_for_suggestion():  
    all_data = get_all_earn_data()
    all_items = all_data.items() 
    total_spent_since_start_earn_date = sum(Decimal(item[1]["spent_since_start_earn_date"]) for item in all_items) 
    
    # Calculate the number of days from the start date until today
    current_date = datetime.now()
    num_days = (current_date - earn_start_date).days + 1  # Include the start date
    
    # Calculate the maximum amount that can be spent from the start date until today
    max_spend = Decimal(num_days * minimum_earn_balance)

    difference = max_spend - total_spent_since_start_earn_date
    
    total_days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    number_of_left_days_in_month = total_days_in_month - current_date.day 
    number_of_days_in_next_month = calendar.monthrange(current_date.year, current_date.month + 1)[1]
    total_days_for_rebalance = number_of_left_days_in_month + number_of_days_in_next_month
    return Decimal(minimum_earn_balance) + (difference / Decimal(total_days_for_rebalance) or Decimal(0))


 
def buy_coin(client, coin, purchase_amount): 
    try:
        coin_value = coin.value
        symbol = f"{coin_value}USDT"
        price_info = client.get_symbol_ticker(symbol=symbol)
        price = float(price_info['price'])
        print(symbol)
        # Calculate the amount of the coin that can be bought
        round_to = coins_round_to.get(coin, 5)  # Default to 5 decimal places if coin not found 
        print(f"round_to={round_to}")
        amount = round(Decimal(purchase_amount) / Decimal(price), round_to) 
        # Print the order details
        print(f"symbol={symbol}, side={Client.SIDE_BUY}, type={Client.ORDER_TYPE_MARKET}, quantity={amount}")
        
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=amount
        )

        print(order)
        if order and 'orderId' in order:
            # Add order data to the database
            transact_time = datetime.fromtimestamp(order['transactTime'] / 1000).strftime('%Y-%m-%d')
            fills = order['fills'][0]
            qty = float(fills['qty'])
            price = float(fills['price'])
            # Extract the commission from the order
            commission_rate = sum(float(fill['commission']) for fill in order['fills'])
            commission = round(float(price) * commission_rate, 8)
            total = float(order['cummulativeQuoteQty'])  
            insert_coin_purchase(coin_value, transact_time, qty, price, total, commission)
            
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
    # order = {'symbol': 'ETHUSDT', 'orderId': 20692862175, 'orderListId': -1, 'clientOrderId': 'HeXTB1hT8iUzWlxncJthsY', 'transactTime': 1728810539104, 'price': '0.00000000', 'origQty': '0.00220000', 'executedQty': '0.00220000', 'cummulativeQuoteQty': '5.42476000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'MARKET', 'side': 'BUY', 'workingTime': 1728810539104, 'fills': [{'price': '2465.80000000', 'qty': '0.00220000', 'commission': '0.00000220', 'commissionAsset': 'ETH', 'tradeId': 1641237218}], 'selfTradePreventionMode': 'EXPIRE_MAKER'}
    # transact_time = datetime.fromtimestamp(order['transactTime'] / 1000).strftime('%Y-%m-%d')
    # fills = order['fills'][0]
    # qty = float(fills['qty'])
    # price = float(fills['price'])
    # # Extract the commission from the order
    # commission_rate = sum(float(fill['commission']) for fill in order['fills'])
    # commission = round(float(price) * commission_rate, 8)
    # total = float(order['cummulativeQuoteQty'])  
    # print(f"transact_time={transact_time}, qty={qty}, price={price}, total={total}, commission={commission}")
    amount = select_purchase_amount_for_suggestion()
    print(f"amount={amount}")
        
        


