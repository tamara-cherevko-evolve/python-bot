
from time import sleep
from binance.client import Client
from flask import Flask, jsonify 
from flask_cors import CORS 
from waitress import serve
from constants import *
from create_order import get_price_btcusd
from ballance import get_balance_usdt, get_minimum_balance, check_balance_for_orders
import requests
from dotenv import load_dotenv
import os

load_dotenv() 

from orders import recalculate_sell_order, start_listening_orders 

app = Flask(__name__) 
CORS(app) 
client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET")) 
 
@app.route('/')
def index():
    return jsonify({"status": "index"}), 200

@app.route('/get-balance', methods=['GET'])
def get_balance():   
    try: 
        balance = get_balance_usdt(client)  
        price = get_price_btcusd(client)
        minimum_balance = get_minimum_balance(price)
        is_ballance_enough = check_balance_for_orders(client, price) 
        return jsonify({"balance": balance, "minimum_balance": minimum_balance, "is_ballance_enough": is_ballance_enough}), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/start-dca-grid', methods=['GET'])
def start_dca_grid():   
    try: 
        balance = get_balance_usdt(client)  
        # data = start_DCA_grid(client) 
        return jsonify({"status": balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/start-listen-orders', methods=['GET'])
def start_listen():  
    start_listening_orders(client)
    return jsonify({"status": "Listening orders started"}), 200 


@app.route('/recalculate-sell-order', methods=['POST'])
def recalculate_order():  
    recalculate_sell_order(client) 
    sleep(1)
    return jsonify({"status": "Order recalculated"}), 200


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8000) 

