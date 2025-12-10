#!/usr/bin/env python3
"""
Crypto Trading Bot Backend - Flask API
Optimized for Vercel serverless deployment
"""

import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

# App initialization
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Bot status
BOT_AVAILABLE = True

# ===== ROOT ROUTE =====

@app.route('/')
def root():
    """Root endpoint - returns API info."""
    return jsonify({
        'name': 'Crypto Trading Bot API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': [
            '/api/status',
            '/api/symbols',
            '/api/price/<symbol>',
            '/api/orders',
            '/api/trades/<symbol>',
            '/api/account'
        ]
    })

# ===== API ROUTES =====

@app.route('/api/status')
def get_status():
    """Get bot connection status."""
    return jsonify({
        'connected': BOT_AVAILABLE,
        'timestamp': int(time.time() * 1000),
        'demo_mode': True,
        'message': 'Crypto Trading Bot API'
    })

@app.route('/api/symbols')
def get_symbols():
    """Get available trading symbols."""
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
    return jsonify({'symbols': symbols})

@app.route('/api/price/<symbol>')
def get_symbol_price(symbol):
    """Get current price for a symbol with real-time fluctuations."""
    # Base demo data for common symbols
    demo_prices = {
        'BTCUSDT': {
            'symbol': 'BTCUSDT',
            'base_price': 52340.50,
            'bid_price': 52335.00,
            'ask_price': 52346.00,
            'high_24h': 53200.00,
            'low_24h': 50150.75,
            'volume_24h': '1.2M',
            'base_change': 1200.50,
            'base_change_percent': 2.50
        },
        'ETHUSDT': {
            'symbol': 'ETHUSDT',
            'base_price': 3145.80,
            'bid_price': 3143.50,
            'ask_price': 3148.10,
            'high_24h': 3220.00,
            'low_24h': 3080.50,
            'volume_24h': '2.5M',
            'base_change': 52.80,
            'base_change_percent': 1.75
        },
        'BNBUSDT': {
            'symbol': 'BNBUSDT',
            'base_price': 625.40,
            'bid_price': 624.50,
            'ask_price': 626.30,
            'high_24h': 645.00,
            'low_24h': 610.25,
            'volume_24h': '5M',
            'base_change': -5.60,
            'base_change_percent': -0.85
        },
        'SOLUSDT': {
            'symbol': 'SOLUSDT',
            'base_price': 185.20,
            'bid_price': 184.80,
            'ask_price': 185.60,
            'high_24h': 192.50,
            'low_24h': 178.75,
            'volume_24h': '10M',
            'base_change': 5.60,
            'base_change_percent': 3.20
        },
        'ADAUSDT': {
            'symbol': 'ADAUSDT',
            'base_price': 1.02,
            'bid_price': 1.01,
            'ask_price': 1.03,
            'high_24h': 1.08,
            'low_24h': 0.98,
            'volume_24h': '50M',
            'base_change': -0.02,
            'base_change_percent': -1.25
        }
    }
    
    if symbol not in demo_prices:
        return jsonify({'error': 'Symbol not found'}), 404
    
    data = demo_prices[symbol].copy()
    
    # Add realistic price fluctuation (±0.5% of base price)
    fluctuation_percent = random.uniform(-0.5, 0.5)
    base_price = data['base_price']
    price_change = base_price * (fluctuation_percent / 100)
    current_price = base_price + price_change
    
    # Update prices with fluctuation
    return jsonify({
        'symbol': data['symbol'],
        'current_price': round(current_price, 2),
        'bid_price': round(current_price - 5, 2),
        'ask_price': round(current_price + 5, 2),
        'high_24h': data['high_24h'],
        'low_24h': data['low_24h'],
        'volume_24h': data['volume_24h'],
        'price_change_24h': round(data['base_change'] + price_change, 2),
        'price_change_percent_24h': round(data['base_change_percent'] + fluctuation_percent, 2),
        'timestamp': int(time.time() * 1000)
    })

@app.route('/api/trades/<symbol>')
def get_recent_trades(symbol):
    """Get recent trades for a symbol."""
    trades = [
        {
            'id': '1',
            'symbol': symbol,
            'type': 'BUY',
            'quantity': 0.25,
            'price': 49500,
            'time': '2:30 PM',
            'pnl': '+$150'
        },
        {
            'id': '2',
            'symbol': symbol,
            'type': 'SELL',
            'quantity': 0.5,
            'price': 50500,
            'time': '1:45 PM',
            'pnl': '+$250'
        }
    ]
    return jsonify(trades)

@app.route('/api/orders')
def get_orders():
    """Get open orders."""
    symbol = request.args.get('symbol', 'BTCUSDT')
    orders = [
        {
            'id': '1',
            'symbol': symbol,
            'type': 'LIMIT',
            'side': 'BUY',
            'quantity': 0.5,
            'price': 49000,
            'status': 'OPEN'
        },
        {
            'id': '2',
            'symbol': symbol,
            'type': 'LIMIT',
            'side': 'SELL',
            'quantity': 1.0,
            'price': 51000,
            'status': 'OPEN'
        }
    ]
    return jsonify(orders)

@app.route('/api/account')
def get_account():
    """Get account information."""
    return jsonify({
        'balance': 10000.00,
        'available': 9500.00,
        'pnl': 500.00,
        'pnl_percent': 5.0,
        'total_trades': 25,
        'win_rate': 65.0
    })

@app.route('/api/export')
def export_data():
    """Export trading data as CSV."""
    csv_data = "Date,Symbol,Type,Quantity,Price,PnL\n"
    csv_data += "2024-12-10,BTCUSDT,BUY,0.25,49500,+$150\n"
    csv_data += "2024-12-10,BTCUSDT,SELL,0.5,50500,+$250\n"
    return csv_data, 200, {'Content-Type': 'text/csv'}

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Not found',
        'path': request.path,
        'method': request.method,
        'message': 'Endpoint does not exist. Try /api/status or / for available endpoints'
    }), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'details': str(error)
    }), 500

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
