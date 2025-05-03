from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

# Получение символа по адресу или ссылке
@app.route('/get_symbol', methods=['GET'])
def get_symbol():
    raw_input = request.args.get('address')
    if not raw_input:
        return jsonify({'error': 'No address provided'}), 400

    # Если это ссылка вида https://mexc.com/ru-RU/exchange/SHIRO_USDT
    match = re.search(r'exchange/([A-Z0-9_]+)', raw_input)
    if match:
        return jsonify({'symbol': match.group(1)})

    # Если это просто имя токена, например SHIRO
    if re.fullmatch(r'[A-Z0-9]{2,10}', raw_input.upper()):
        return jsonify({'symbol': raw_input.upper() + '_USDT'})

    # Если это адрес контракта 0x...
    if raw_input.startswith('0x'):
        try:
            response = requests.get("https://www.mexc.com/open/api/v2/market/symbols")
            data = response.json()
            for pair in data.get("data", []):
                if pair.get("baseToken", "").lower() == raw_input.lower():
                    return jsonify({'symbol': pair["symbol"]})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return jsonify({'error': 'symbol_not_found'}), 404

    return jsonify({'error': 'Invalid input'}), 400

# Получение стакана и тикера
@app.route('/get_orderbook', methods=['GET'])
def get_orderbook():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({'error': 'No symbol provided'}), 400

    try:
        depth_res = requests.get(f"https://www.mexc.com/open/api/v2/market/depth?symbol={symbol}&depth=20")
        ticker_res = requests.get(f"https://www.mexc.com/open/api/v2/market/ticker?symbol={symbol}")

        return jsonify({
            'depth': depth_res.json().get('data', {}),
            'ticker': ticker_res.json().get('data', {})
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
