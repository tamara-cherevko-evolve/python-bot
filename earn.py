from decimal import Decimal
from constants import coins_titles, Coin
from db import get_all_earn_data

def select_coin_for_suggestion(): 

    all_data = get_all_earn_data()
    # Find the coin with the lowest earnings total
    lowest_earning_coin = min(all_data.items(), key=lambda x: Decimal(x[1]['diff_in_percent']))
 
    return lowest_earning_coin[1]

# Example usage
if __name__ == "__main__":
    suggested_coin = select_coin_for_suggestion()
    print(f"Suggested coin for buy: {suggested_coin}")