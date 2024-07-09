from constants import *

def calculate_nex_DCA_price(price, index):
    return round(price - (price*(sl*index)), 2)

def calculate_price_with_commission(avg_price, total_quantity, tp_price):
    return round((total_quantity/1000*avg_price+total_quantity/1000*tp_price)/(total_quantity)+tp_price, 2)

def calculate_take_profit_price_without_commission(price, total_quantity, multiplier=1):
    tp_price = round(price + (price*tp/(total_quantity/buy_qty)*multiplier), 2) 
    return tp_price

def calculate_take_profit_price(price, total_quantity, multiplier=1):
    tp_price = calculate_take_profit_price_without_commission(price, total_quantity, multiplier)
    tp_price_with_commission = calculate_price_with_commission(price, total_quantity, tp_price)
    return tp_price_with_commission
 
def calculate_avg_price(orders):
    total_spent = sum(float(order['cummulativeQuoteQty']) for order in orders)
    count = len(orders)
    average_price = total_spent / buy_qty / count
    return round(average_price, 2)

def calculate_total_quantity(orders):
    total_quantity = round(sum(float(order['executedQty']) for order in orders), 4)
    return total_quantity

def calculate_total_spent(orders):
    total_spent = sum(float(order['cummulativeQuoteQty']) for order in orders)
    return round(total_spent, 2)

def calculate_expected_profit(orders): 
    avg_price = calculate_avg_price(orders)
    total_quantity = calculate_total_quantity(orders)
    tp_price = calculate_take_profit_price_without_commission(avg_price, total_quantity)
    total_spent = calculate_total_spent(orders)
    expected_income = float(total_quantity*tp_price)
    return round(expected_income - total_spent, 2)