#!/usr/bin/env python3
"""
Simple Flask server to serve the trading bot frontend
and provide API endpoints for the bot functionality.
"""

import os
import sys
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import time
import random
from datetime import datetime

# Add the parent directory to the path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.basic_bot import BasicBot
from bot.order_handler import OrderHandler

app = Flask(__name__)
CORS(app)

# Initialize bot components
bot = BasicBot()
order_handler = OrderHandler(bot.client)

@app.route('/')
def index():
    """Serve the main trading interface."""
    return send_from_directory('.', 'index.html')

@app.route('/signin')
def signin():
    """Serve the signin page."""
    return send_from_directory('.', 'signin.html')

@app.route('/signup')
def signup():
    """Serve the signup page."""
    return send_from_directory('.', 'signup.html')

@app.route('/profile')
def profile():
    """Serve the profile page."""
    return send_from_directory('.', 'profile.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files."""
    return send_from_directory('.', filename)

@app.route('/api/status')
def get_status():
    """Get bot connection status."""
    return jsonify({
        'connected': True,
        'timestamp': int(time.time() * 1000),
        'demo_mode': True
    })

@app.route('/api/symbols')
def get_symbols():
    """Get available trading symbols."""
    try:
        exchange_info = bot.client.futures_exchange_info()
        symbols = [symbol['symbol'] for symbol in exchange_info['symbols'] if symbol['status'] == 'TRADING']
        return jsonify(symbols)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/price/<symbol>')
def get_symbol_price(symbol):
    """Get current price for a symbol."""
    try:
        price_data = bot.get_symbol_price(symbol)
        return jsonify(price_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trades/<symbol>')
def get_recent_trades(symbol):
    """Get recent trades for a symbol."""
    try:
        limit = request.args.get('limit', 10, type=int)
        trades = bot.get_recent_trades(symbol, limit)
        return jsonify(trades)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/klines/<symbol>')
def get_klines(symbol):
    """Get klines/candlestick data for a symbol."""
    try:
        interval = request.args.get('interval', '1h')
        limit = request.args.get('limit', 100, type=int)
        klines = bot.get_klines(symbol, interval, limit)
        return jsonify(klines)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/account')
def get_account_info():
    """Get account information."""
    try:
        account_info = bot.get_account_info()
        return jsonify(account_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/balance/<asset>')
def get_balance(asset):
    """Get balance for a specific asset."""
    try:
        balance = bot.get_balance(asset)
        return jsonify(balance)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_open_orders():
    """Get open orders."""
    try:
        symbol = request.args.get('symbol')
        orders = order_handler.get_open_orders(symbol)
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def place_order():
    """Place a new order."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['symbol', 'side', 'type', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Place order based on type
        if data['type'] == 'MARKET':
            result = order_handler.place_market_order(
                data['symbol'], data['side'], data['quantity']
            )
        elif data['type'] == 'LIMIT':
            if 'price' not in data:
                return jsonify({'error': 'Price is required for limit orders'}), 400
            result = order_handler.place_limit_order(
                data['symbol'], data['side'], data['quantity'], data['price']
            )
        elif data['type'] == 'STOP_LIMIT':
            if 'price' not in data or 'stop_price' not in data:
                return jsonify({'error': 'Price and stop_price are required for stop-limit orders'}), 400
            result = order_handler.place_stop_limit_order(
                data['symbol'], data['side'], data['quantity'], 
                data['stop_price'], data['price']
            )
        else:
            return jsonify({'error': f'Unsupported order type: {data["type"]}'}), 400
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<order_id>', methods=['DELETE'])
def cancel_order(order_id):
    """Cancel an order."""
    try:
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        result = order_handler.cancel_order(symbol, order_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<order_id>')
def get_order_status(order_id):
    """Get order status."""
    try:
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({'error': 'Symbol is required'}), 400
        
        result = order_handler.get_order_status(symbol, order_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/positions/close', methods=['POST'])
def close_all_positions():
    """Close all positions."""
    try:
        result = bot.close_all_positions()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/cancel-all', methods=['POST'])
def cancel_all_orders():
    """Cancel all orders."""
    try:
        symbol = request.args.get('symbol')
        result = bot.cancel_all_orders(symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/symbols/<symbol>/info')
def get_symbol_info(symbol):
    """Get symbol information."""
    try:
        info = bot.get_symbol_info(symbol)
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Crypto Trading Bot Frontend Server...")
    print("Open http://localhost:5000 in your browser")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    ) 