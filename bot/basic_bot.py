import os
import time
import random
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from dotenv import load_dotenv

from .order_handler import OrderHandler
from .logger import logger
from .utils import validate_symbol, get_symbol_info

# Load environment variables
load_dotenv()

class DemoClient:
    """Demo client that simulates Binance API responses."""
    
    def __init__(self):
        self.demo_mode = True
        self.orders = {}
        self.positions = {}
        self.account_balance = {
            'USDT': {
                'walletBalance': '10000.00',
                'unrealizedPnl': '0.00',
                'marginBalance': '10000.00',
                'availableBalance': '10000.00'
            }
        }
        self.order_counter = 1000
    
    def get_server_time(self):
        """Get server time."""
        return {'serverTime': int(time.time() * 1000)}
    
    def futures_ticker(self, symbol):
        """Get ticker information."""
        # Simulate realistic price data
        base_price = {
            'BTCUSDT': 50000,
            'ETHUSDT': 3000,
            'ADAUSDT': 0.5,
            'BNBUSDT': 400,
            'SOLUSDT': 100
        }.get(symbol, 100)
        
        # Add some random variation
        variation = random.uniform(-0.02, 0.02)  # ±2%
        current_price = base_price * (1 + variation)
        
        return {
            'symbol': symbol,
            'lastPrice': f"{current_price:.2f}",
            'bidPrice': f"{current_price * 0.999:.2f}",
            'askPrice': f"{current_price * 1.001:.2f}",
            'highPrice': f"{current_price * 1.05:.2f}",
            'lowPrice': f"{current_price * 0.95:.2f}",
            'volume': f"{random.uniform(1000, 10000):.2f}",
            'priceChange': f"{current_price * random.uniform(-0.1, 0.1):.2f}",
            'priceChangePercent': f"{random.uniform(-5, 5):.2f}"
        }
    
    def futures_exchange_info(self):
        """Get exchange information."""
        return {
            'symbols': [
                {
                    'symbol': 'BTCUSDT',
                    'status': 'TRADING',
                    'baseAsset': 'BTC',
                    'quoteAsset': 'USDT',
                    'pricePrecision': 2,
                    'quantityPrecision': 3
                },
                {
                    'symbol': 'ETHUSDT',
                    'status': 'TRADING',
                    'baseAsset': 'ETH',
                    'quoteAsset': 'USDT',
                    'pricePrecision': 2,
                    'quantityPrecision': 3
                },
                {
                    'symbol': 'ADAUSDT',
                    'status': 'TRADING',
                    'baseAsset': 'ADA',
                    'quoteAsset': 'USDT',
                    'pricePrecision': 4,
                    'quantityPrecision': 1
                }
            ]
        }
    
    def futures_recent_trades(self, symbol, limit=10):
        """Get recent trades."""
        trades = []
        base_price = float(self.futures_ticker(symbol)['lastPrice'])
        
        for i in range(limit):
            price_variation = random.uniform(-0.01, 0.01)
            price = base_price * (1 + price_variation)
            quantity = random.uniform(0.001, 1.0)
            
            trades.append({
                'id': random.randint(1000000, 9999999),
                'price': f"{price:.2f}",
                'qty': f"{quantity:.3f}",
                'time': int(time.time() * 1000) - i * 60000,  # 1 minute apart
                'isBuyerMaker': random.choice([True, False])
            })
        
        return trades
    
    def futures_klines(self, symbol, interval='1h', limit=100):
        """Get kline data."""
        klines = []
        base_price = float(self.futures_ticker(symbol)['lastPrice'])
        
        for i in range(limit):
            # Simulate OHLCV data
            open_price = base_price * random.uniform(0.95, 1.05)
            high_price = open_price * random.uniform(1.0, 1.1)
            low_price = open_price * random.uniform(0.9, 1.0)
            close_price = random.uniform(low_price, high_price)
            volume = random.uniform(100, 1000)
            
            # Calculate time based on interval
            if interval == '1h':
                time_offset = i * 3600
            elif interval == '1d':
                time_offset = i * 86400
            else:
                time_offset = i * 3600  # Default to 1h
            
            klines.append([
                int(time.time() * 1000) - time_offset * 1000,  # Open time
                f"{open_price:.2f}",  # Open
                f"{high_price:.2f}",  # High
                f"{low_price:.2f}",   # Low
                f"{close_price:.2f}", # Close
                f"{volume:.2f}",      # Volume
                int(time.time() * 1000) - time_offset * 1000 + 3600000,  # Close time
                f"{random.uniform(100, 1000):.2f}",  # Quote asset volume
                0,  # Number of trades
                f"{random.uniform(100, 1000):.2f}",  # Taker buy base asset volume
                f"{random.uniform(100, 1000):.2f}"   # Taker buy quote asset volume
            ])
        
        return klines
    
    def futures_account(self):
        """Get account information."""
        return {
            'canTrade': True,
            'canWithdraw': True,
            'canDeposit': True,
            'updateTime': int(time.time() * 1000),
            'assets': [
                {
                    'asset': 'USDT',
                    'walletBalance': '10000.00',
                    'unrealizedPnl': '0.00',
                    'marginBalance': '10000.00',
                    'availableBalance': '10000.00'
                }
            ],
            'positions': [
                {
                    'symbol': 'BTCUSDT',
                    'positionAmt': '0.000',
                    'entryPrice': '0.00',
                    'markPrice': '0.00',
                    'unRealizedProfit': '0.00'
                },
                {
                    'symbol': 'ETHUSDT',
                    'positionAmt': '0.000',
                    'entryPrice': '0.00',
                    'markPrice': '0.00',
                    'unRealizedProfit': '0.00'
                }
            ]
        }

class BasicBot:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, 
                 testnet: bool = False):
        """
        Initialize the BasicBot with demo mode.
        
        Args:
            api_key: Not used in demo mode
            api_secret: Not used in demo mode
            testnet: Not used in demo mode
        """
        # Demo mode is always enabled
        self.demo_mode = True
        self.testnet = False
        
        # Initialize demo client
        self.client = DemoClient()
        
        # Initialize order handler
        self.order_handler = OrderHandler(self.client)
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self):
        """Test the connection to demo API."""
        try:
            # Get server time to test connection
            server_time = self.client.get_server_time()
            logger.info(f"Successfully connected to Demo API. Server time: {server_time}")
            logger.info("Demo mode enabled - All operations are simulated")
            logger.info("Available operations: Market data, price info, symbol info, simulated trading")
            
        except Exception as e:
            logger.error(f"Failed to connect to Demo API: {e}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        return self.order_handler.get_account_info()
    
    def get_balance(self, asset: str = 'USDT') -> Dict[str, Any]:
        """Get balance for a specific asset."""
        try:
            account_info = self.get_account_info()
            balances = account_info.get('assets', [])
            
            for balance in balances:
                if balance.get('asset') == asset:
                    return {
                        'asset': asset,
                        'wallet_balance': balance.get('walletBalance'),
                        'unrealized_pnl': balance.get('unrealizedPnl'),
                        'margin_balance': balance.get('marginBalance'),
                        'available_balance': balance.get('availableBalance')
                    }
            
            logger.warning(f"Asset {asset} not found in account")
            return {}
            
        except Exception as e:
            logger.error(f"Error getting balance for {asset}: {e}")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: str) -> Dict[str, Any]:
        """Place a market order."""
        return self.order_handler.place_market_order(symbol, side, quantity)
    
    def place_limit_order(self, symbol: str, side: str, quantity: str, 
                         price: str, time_in_force: str = 'GTC') -> Dict[str, Any]:
        """Place a limit order."""
        return self.order_handler.place_limit_order(symbol, side, quantity, price, time_in_force)
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: str,
                              stop_price: str, limit_price: str, 
                              time_in_force: str = 'GTC') -> Dict[str, Any]:
        """Place a stop-limit order."""
        return self.order_handler.place_stop_limit_order(
            symbol, side, quantity, stop_price, limit_price, time_in_force
        )
    
    def place_oco_order(self, symbol: str, side: str, quantity: str,
                       price: str, stop_price: str, stop_limit_price: str) -> Dict[str, Any]:
        """Place an OCO (One-Cancels-Other) order."""
        return self.order_handler.place_oco_order(
            symbol, side, quantity, price, stop_price, stop_limit_price
        )
    
    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order."""
        return self.order_handler.cancel_order(symbol, order_id)
    
    def get_order_status(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Get the status of an order."""
        return self.order_handler.get_order_status(symbol, order_id)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """Get all open orders."""
        return self.order_handler.get_open_orders(symbol)
    
    def get_symbol_price(self, symbol: str) -> Dict[str, Any]:
        """Get current price for a symbol."""
        try:
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            logger.info(f"Getting current price for {symbol}")
            
            # Get 24hr ticker price change statistics
            ticker = self.client.futures_ticker(symbol=symbol.upper())
            
            price_info = {
                'symbol': symbol.upper(),
                'current_price': ticker.get('lastPrice'),
                'bid_price': ticker.get('bidPrice'),
                'ask_price': ticker.get('askPrice'),
                'high_24h': ticker.get('highPrice'),
                'low_24h': ticker.get('lowPrice'),
                'volume_24h': ticker.get('volume'),
                'price_change_24h': ticker.get('priceChange'),
                'price_change_percent_24h': ticker.get('priceChangePercent')
            }
            
            logger.info(f"Current price for {symbol}: {price_info['current_price']}")
            return price_info
            
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get detailed information about a symbol."""
        try:
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            logger.info(f"Getting symbol info for {symbol}")
            
            # Get exchange info
            exchange_info = self.client.futures_exchange_info()
            
            for symbol_info in exchange_info.get('symbols', []):
                if symbol_info.get('symbol') == symbol.upper():
                    return {
                        'symbol': symbol_info.get('symbol'),
                        'status': symbol_info.get('status'),
                        'baseAsset': symbol_info.get('baseAsset'),
                        'quoteAsset': symbol_info.get('quoteAsset'),
                        'pricePrecision': symbol_info.get('pricePrecision'),
                        'quantityPrecision': symbol_info.get('quantityPrecision'),
                        'filters': symbol_info.get('filters', [])
                    }
            
            raise ValueError(f"Symbol {symbol} not found")
            
        except Exception as e:
            logger.error(f"Error getting symbol info for {symbol}: {e}")
            raise
    
    def get_recent_trades(self, symbol: str, limit: int = 10) -> list:
        """Get recent trades for a symbol."""
        try:
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if limit < 1 or limit > 1000:
                raise ValueError("Limit must be between 1 and 1000")
            
            logger.info(f"Getting recent trades for {symbol}")
            
            response = self.client.futures_recent_trades(symbol=symbol.upper(), limit=limit)
            logger.info(f"Retrieved {len(response)} recent trades for {symbol}")
            return response
            
        except Exception as e:
            logger.error(f"Error getting recent trades for {symbol}: {e}")
            raise
    
    def get_klines(self, symbol: str, interval: str = '1h', limit: int = 100) -> list:
        """Get kline/candlestick data for a symbol."""
        try:
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            valid_intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
            if interval not in valid_intervals:
                raise ValueError(f"Invalid interval. Must be one of: {valid_intervals}")
            
            if limit < 1 or limit > 1000:
                raise ValueError("Limit must be between 1 and 1000")
            
            logger.info(f"Getting klines for {symbol} with interval {interval}")
            
            response = self.client.futures_klines(symbol=symbol.upper(), interval=interval, limit=limit)
            logger.info(f"Retrieved {len(response)} klines for {symbol}")
            return response
            
        except Exception as e:
            logger.error(f"Error getting klines for {symbol}: {e}")
            raise
    
    def close_all_positions(self) -> Dict[str, Any]:
        """Close all open positions."""
        try:
            logger.info("Closing all open positions")
            
            # Get account info to find open positions
            account_info = self.get_account_info()
            positions = account_info.get('positions', [])
            
            closed_positions = []
            for position in positions:
                if float(position.get('positionAmt', 0)) != 0:
                    symbol = position.get('symbol')
                    side = 'SELL' if float(position.get('positionAmt', 0)) > 0 else 'BUY'
                    quantity = abs(float(position.get('positionAmt', 0)))
                    
                    if quantity > 0:
                        try:
                            result = self.place_market_order(symbol, side, str(quantity))
                            closed_positions.append({
                                'symbol': symbol,
                                'side': side,
                                'quantity': quantity,
                                'result': result
                            })
                            logger.info(f"Closed position: {symbol} {side} {quantity}")
                        except Exception as e:
                            logger.error(f"Failed to close position {symbol}: {e}")
            
            logger.info(f"Closed {len(closed_positions)} positions")
            return {'closed_positions': closed_positions}
            
        except Exception as e:
            logger.error(f"Error closing all positions: {e}")
            raise
    
    def cancel_all_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Cancel all open orders."""
        try:
            logger.info(f"Cancelling all open orders{f' for {symbol}' if symbol else ''}")
            
            # Get open orders
            open_orders = self.get_open_orders(symbol)
            
            cancelled_orders = []
            for order in open_orders:
                try:
                    result = self.cancel_order(order['symbol'], order['order_id'])
                    cancelled_orders.append({
                        'symbol': order['symbol'],
                        'order_id': order['order_id'],
                        'result': result
                    })
                    logger.info(f"Cancelled order: {order['symbol']} {order['order_id']}")
                except Exception as e:
                    logger.error(f"Failed to cancel order {order['order_id']}: {e}")
            
            logger.info(f"Cancelled {len(cancelled_orders)} orders")
            return {'cancelled_orders': cancelled_orders}
            
        except Exception as e:
            logger.error(f"Error cancelling all orders: {e}")
            raise
