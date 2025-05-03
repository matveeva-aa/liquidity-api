from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # ← это ключ

@app.route('/get_symbol')
def get_symbol():
    address = request.args.get('address')
    if not address:
        return {"error": "No address"}, 400
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/contract/{address}"
    r = requests.get(url)
    return r.json()

@app.route('/get_orderbook')
def get_orderbook():
    symbol = request.args.get('symbol')
    if not symbol:
        return {"error": "No symbol"}, 400
    book_url = f"https://api.mexc.com/api/v3/depth?symbol={symbol}USDT&limit=50"
    ticker_url = f"https://api.mexc.com/api/v3/ticker/24hr?symbol={symbol}USDT"
    book = requests.get(book_url).json()
    ticker = requests.get(ticker_url).json()
    return jsonify({"depth": book, "ticker": ticker})

if __name__ == '__main__':
    app.run(port=5000)
