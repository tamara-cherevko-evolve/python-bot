
from time import sleep
from binance.client import Client
from flask import Flask, jsonify, render_template 
from flask_cors import CORS 
from waitress import serve
from constants import *
from create_order import start_DCA_grid
from flask_sqlalchemy import SQLAlchemy
import requests
from dotenv import load_dotenv
import os

load_dotenv()
 
from orders import recalculate_sell_order, start_listening_orders 

app = Flask(__name__) 
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET")) 
 
@app.route('/')
def index():
    return jsonify({"status": "index"}), 200

@app.route('/start-dca-grid', methods=['GET'])
def start_dca_grid():  
    print(f"API_KEY: {os.getenv('API_KEY')}")
    print(f"API_SECRET: {os.getenv('API_SECRET')}") 
    account_details = client.get_account()
    # data = start_DCA_grid(client) 
    return jsonify({"status": account_details}), 200

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

