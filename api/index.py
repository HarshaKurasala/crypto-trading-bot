#!/usr/bin/env python3
"""
Vercel-compatible Flask server for Crypto Trading Bot
This version is optimized for Vercel serverless deployment
"""

import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from datetime import datetime

# Get the base path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

# Add parent directory to path for bot imports
sys.path.insert(0, BASE_DIR)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize bot only if available
BOT_AVAILABLE = False
try:
    from bot.basic_bot import BasicBot
    from bot.order_handler import OrderHandler
    bot = BasicBot()
    order_handler = OrderHandler(bot.client)
    BOT_AVAILABLE = True
except Exception as e:
    print(f"Warning: Bot initialization skipped: {e}")

# ===== FRONTEND ROUTES =====
@app.route('/')
def index():
    """Serve the main trading interface."""
    try:
        if os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')):
            with open(os.path.join(FRONTEND_DIR, 'index.html'), 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return jsonify({'error': 'index.html not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signin')
def signin():
    """Serve the signin page."""
    try:
        if os.path.exists(os.path.join(FRONTEND_DIR, 'signin.html')):
            with open(os.path.join(FRONTEND_DIR, 'signin.html'), 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return jsonify({'error': 'signin.html not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/signup')
def signup():
    """Serve the signup page."""
    try:
        if os.path.exists(os.path.join(FRONTEND_DIR, 'signup.html')):
            with open(os.path.join(FRONTEND_DIR, 'signup.html'), 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return jsonify({'error': 'signup.html not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/profile')
def profile():
    """Serve the profile page."""
    try:
        if os.path.exists(os.path.join(FRONTEND_DIR, 'profile.html')):
            with open(os.path.join(FRONTEND_DIR, 'profile.html'), 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return jsonify({'error': 'profile.html not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files from frontend directory."""
    try:
        file_path = os.path.join(FRONTEND_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': f'{filename} not found'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Set appropriate content type
        if filename.endswith('.css'):
            return content, 200, {'Content-Type': 'text/css'}
        elif filename.endswith('.js'):
            return content, 200, {'Content-Type': 'application/javascript'}
        elif filename.endswith('.json'):
            return content, 200, {'Content-Type': 'application/json'}
        else:
            return content, 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    """Get current price for a symbol."""
    # Demo data for common symbols
    demo_prices = {
        'BTCUSDT': {
            'symbol': 'BTCUSDT',
            'current_price': 52340.50,
            'bid_price': 52335.00,
            'ask_price': 52346.00,
            'high_24h': 53200.00,
            'low_24h': 50150.75,
            'volume_24h': '1.2M',
            'price_change_24h': 1200.50,
            'price_change_percent_24h': 2.50
        },
        'ETHUSDT': {
            'symbol': 'ETHUSDT',
            'current_price': 3145.80,
            'bid_price': 3143.50,
            'ask_price': 3148.10,
            'high_24h': 3220.00,
            'low_24h': 3080.50,
            'volume_24h': '2.5M',
            'price_change_24h': 52.80,
            'price_change_percent_24h': 1.75
        },
        'BNBUSDT': {
            'symbol': 'BNBUSDT',
            'current_price': 625.40,
            'bid_price': 624.50,
            'ask_price': 626.30,
            'high_24h': 645.00,
            'low_24h': 610.25,
            'volume_24h': '5M',
            'price_change_24h': -5.60,
            'price_change_percent_24h': -0.85
        },
        'SOLUSDT': {
            'symbol': 'SOLUSDT',
            'current_price': 185.20,
            'bid_price': 184.80,
            'ask_price': 185.60,
            'high_24h': 192.50,
            'low_24h': 178.75,
            'volume_24h': '10M',
            'price_change_24h': 5.60,
            'price_change_percent_24h': 3.20
        },
        'ADAUSDT': {
            'symbol': 'ADAUSDT',
            'current_price': 1.02,
            'bid_price': 1.01,
            'ask_price': 1.03,
            'high_24h': 1.08,
            'low_24h': 0.98,
            'volume_24h': '50M',
            'price_change_24h': -0.02,
            'price_change_percent_24h': -1.25
        }
    }
    
    if symbol in demo_prices:
        return jsonify(demo_prices[symbol])
    
    return jsonify({'error': 'Symbol not found'}), 404

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
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
