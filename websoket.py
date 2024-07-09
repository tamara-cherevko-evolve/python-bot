import json
import ssl
import websocket 
from constants import * 
from file_utils import write_status_to_file

from enum import Enum

class ConnectionStatus(Enum):
    OPENED = "opened"
    CLOSED = "closed" 

def on_message(ws, message):
    try:
        msg = json.loads(message)
        print("msg:", msg)
        if msg['e'] == 'executionReport' and msg['X'] == 'FILLED':
            print("Order filled:", msg)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e} - Received message: {message}")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed") 
    write_status_to_file(file_connection_status, ConnectionStatus.CLOSED)

def on_open(ws):
    print("Connection opened") 
    write_status_to_file(file_connection_status, ConnectionStatus.OPENED)
 

if __name__ == "__main__":
    ws_url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    # Create an SSL context that does not verify the certificate
    ssl_opts = {"cert_reqs": ssl.CERT_NONE}
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    # Pass the SSL context to run_forever
    ws.run_forever(sslopt=ssl_opts)  