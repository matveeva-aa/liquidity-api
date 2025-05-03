from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # разрешаем все кросс-доменные запросы

# Получить символ токена по адресу контракта
@app.route('/get_symbol', methods=['GET'])
def get_symbol():
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'No address provided'}), 400

    # Получение списка пар с MEXC
    try:
        response = requests.get("https://www.mexc.com/open/api/v2/market/symbols")
        data = response.json()
        for pair in data.get("data", []):
            if pair.get("baseToken", "").lower() == address.lower():
                return jsonify({'symbol': pair["symbol"]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'symbol_not_found'}), 404

# Получить стакан и объём по символу
@app.route('/get_orderbook', methods=['GET'])
def get_orderbook():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400

    try:
        depth_res = requests.get(f"https://www.mexc.com/open/api/v2/market/depth?symbol={symbol}&depth=20")
        depth_data = depth_res.json()

        ticker_res = requests.get(f"https://www.mexc.com/open/api/v2/market/ticker?symbol={symbol}")
        ticker_data = ticker_res.json()

        return jsonify({
            'depth': depth_data.get('data', {}),
            'ticker': ticker_data.get('data', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=False)
