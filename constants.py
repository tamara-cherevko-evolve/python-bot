api_key = 'hz2PyMdQWfmBORZiRC0Gmwyh2dL4lT8MbG5q1yafz5HaTK225icbqDOVtWJzZT47'
api_secret = 'grARhksfpQ8aZV626xNOw6BwWEBabxFh3jzZpBbjvdu7mXk0v0PjQ7DpQ10wld9u'
current_symbol = 'BTCUSDT' 

file_orders_in_progress = 'client/src/assets/files/orders_in_progress.json'
file_orders_completed = 'client/src/assets/files/orders_completed.json'
file_connection_status = 'client/src/assets/files/connection_status.json'
file_listening_orders = 'client/src/assets/files/listening_orders.json'
  
tp = 0.005 # +0.5%
sl = 0.005 # -0.5%
buy_qty = 0.0001
multiplier = 1
risk_rate = 0.1 # 10% price down risk
risk_buy_more_times = int(risk_rate / sl)
# how many times to buy more fot avg price = 0.5% * 20 = 10%