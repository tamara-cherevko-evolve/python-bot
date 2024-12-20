
from time import sleep
from binance.client import Client 
from mysql.connector import Error
from flask import Flask, jsonify, request 
from flask_cors import CORS 
from waitress import serve
from constants import coins_titles, Coin, minimum_earn_balance, coins_priority, coins_round_to,coins_icons
from create_order import get_price_btcusd
from ballance import get_balance_usdt, get_minimum_balance, check_balance_for_orders
import requests
from dotenv import load_dotenv
import os

from earn import buy_coin, select_coin_for_suggestion, check_balance_for_earn_investment, select_purchase_amount_for_suggestion

load_dotenv() 
 
from db import get_all_earn_data, get_earn_data
from orders import recalculate_sell_order, start_listening_orders 

app = Flask(__name__) 
CORS(app) 
client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET")) 
 
@app.route('/')
def index():
    return jsonify({"status": "index"}), 200

@app.route('/get-coins', methods=['GET'])
def get_coins():
    coins_list = [{
        "coin": coin.value,
        "title": coins_titles[coin],
        "priority": coins_priority[coin],
        "round_to": coins_round_to[coin], 
    } for coin in Coin] 
    return jsonify(coins_list), 200

@app.route('/get-earn-data/<coin>', methods=['GET'])
def get_earn_data_for_btc(coin):
    try:
        data = get_earn_data(coin)
        return jsonify(data), 200
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/get-earn-summary', methods=['GET'])
def get_earn_summary():
    try:
        data = get_all_earn_data()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500


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
    
@app.route('/get-earn-balance-with-suggestion', methods=['GET'])
def get_earn_balance():   
    try: 
        balance = get_balance_usdt(client)  
        is_ballance_enough = balance >= minimum_earn_balance
        suggested_coin = select_coin_for_suggestion()
        suggested_bid = select_purchase_amount_for_suggestion()
        
        return jsonify({
            "balance": balance,
            "minimum_balance": minimum_earn_balance,
            "is_ballance_enough": is_ballance_enough,
            "suggested_coin": suggested_coin,
            "suggested_bid": suggested_bid
        }), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
    
@app.route('/buy-coin', methods=['POST'])
def buy_coin_request():   
    try: 
        data = request.get_json()
        coin_str = data.get('coin') 
        purchase_amount = data.get('purchaseAmount')

        if not coin_str:
            return jsonify({"status": "error", "message": "Missing 'coin' in request"}), 400 

        if not purchase_amount:
            return jsonify({"status": "error", "message": "Missing 'purchaseAmount' in request"}), 400 
        
        try:
            coin = Coin[coin_str]
        except KeyError:
            return jsonify({"status": "error", "message": f"Invalid coin: {coin_str}"}), 400
        
        balance_data = check_balance_for_earn_investment(client)  
        if not balance_data['is_balance_enough']:
            return jsonify({"status": "error", "message": balance_data["message"]}), 500
        else :
            order = buy_coin(client, coin, purchase_amount) 
            if order and 'orderId' in order:
                return {"status": "success", "order": order}, 200
            else:
                return {"status": "error", "message": order['message']}, 500

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

