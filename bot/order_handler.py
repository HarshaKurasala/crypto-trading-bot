import time
import random
from typing import Dict, Any, Optional, List
from .logger import logger
from .utils import (
    validate_symbol, validate_quantity, validate_price, validate_order_type,
    validate_side, format_quantity, format_price, format_order_response,
    validate_stop_limit_params, calculate_stop_price
)

class OrderHandler:
    def __init__(self, client):
        """Initialize order handler with demo client."""
        self.client = client
        self.logger = logger
        
        # Demo mode is always enabled
        self.demo_mode = True
        
        # Initialize demo order storage
        self.orders = {}
        self.order_counter = 1000
    
    def _generate_order_id(self):
        """Generate a unique order ID."""
        self.order_counter += 1
        return str(self.order_counter)
    
    def _simulate_order_response(self, order_type, symbol, side, quantity, price=None, stop_price=None):
        """Simulate an order response."""
        order_id = self._generate_order_id()
        
        response = {
            'orderId': order_id,
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type,
            'origQty': quantity,
            'status': 'FILLED' if order_type == 'MARKET' else 'NEW',
            'time': int(time.time() * 1000)
        }
        
        if price:
            response['price'] = price
        
        if stop_price:
            response['stopPrice'] = stop_price
        
        # Store order for later reference
        self.orders[order_id] = response
        
        return response
    
    def place_market_order(self, symbol: str, side: str, quantity: str) -> Dict[str, Any]:
        """Place a market order."""
        try:
            # Validate inputs
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if not validate_side(side):
                raise ValueError(f"Invalid side: {side}")
            
            if not validate_quantity(quantity):
                raise ValueError(f"Invalid quantity: {quantity}")
            
            # Format quantity
            formatted_qty = format_quantity(quantity)
            
            # Place order
            self.logger.info(f"Placing market {side} order for {formatted_qty} {symbol}")
            
            # Simulate order placement
            response = self._simulate_order_response('MARKET', symbol, side, formatted_qty)
            
            # Log the order
            self.logger.order_placed('MARKET', symbol, formatted_qty)
            self.logger.api_call('futures_create_order', {
                'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': formatted_qty
            }, response)
            
            return format_order_response(response)
            
        except Exception as e:
            self.logger.error(f"Error placing market order: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: str, 
                         price: str, time_in_force: str = 'GTC') -> Dict[str, Any]:
        """Place a limit order."""
        try:
            # Validate inputs
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if not validate_side(side):
                raise ValueError(f"Invalid side: {side}")
            
            if not validate_quantity(quantity):
                raise ValueError(f"Invalid quantity: {quantity}")
            
            if not validate_price(price):
                raise ValueError(f"Invalid price: {price}")
            
            # Format inputs
            formatted_qty = format_quantity(quantity)
            formatted_price = format_price(price)
            
            # Place order
            self.logger.info(f"Placing limit {side} order for {formatted_qty} {symbol} @ {formatted_price}")
            
            # Simulate order placement
            response = self._simulate_order_response('LIMIT', symbol, side, formatted_qty, formatted_price)
            
            # Log the order
            self.logger.order_placed('LIMIT', symbol, formatted_qty, formatted_price)
            self.logger.api_call('futures_create_order', {
                'symbol': symbol, 'side': side, 'type': 'LIMIT', 
                'quantity': formatted_qty, 'price': formatted_price
            }, response)
            
            return format_order_response(response)
            
        except Exception as e:
            self.logger.error(f"Error placing limit order: {e}")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: str,
                              stop_price: str, limit_price: str, 
                              time_in_force: str = 'GTC') -> Dict[str, Any]:
        """Place a stop-limit order."""
        try:
            # Validate inputs
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if not validate_side(side):
                raise ValueError(f"Invalid side: {side}")
            
            if not validate_quantity(quantity):
                raise ValueError(f"Invalid quantity: {quantity}")
            
            if not validate_price(stop_price) or not validate_price(limit_price):
                raise ValueError("Invalid stop or limit price")
            
            # Validate stop-limit parameters
            if not validate_stop_limit_params(stop_price, limit_price, side):
                raise ValueError("Invalid stop-limit parameters for the given side")
            
            # Format inputs
            formatted_qty = format_quantity(quantity)
            formatted_stop = format_price(stop_price)
            formatted_limit = format_price(limit_price)
            
            # Place order
            self.logger.info(f"Placing stop-limit {side} order for {formatted_qty} {symbol}")
            self.logger.info(f"Stop: {formatted_stop}, Limit: {formatted_limit}")
            
            # Simulate order placement
            response = self._simulate_order_response('STOP_MARKET', symbol, side, formatted_qty, formatted_limit, formatted_stop)
            
            # Log the order
            self.logger.order_placed('STOP_LIMIT', symbol, formatted_qty)
            self.logger.api_call('futures_create_order', {
                'symbol': symbol, 'side': side, 'type': 'STOP_MARKET',
                'quantity': formatted_qty, 'stopPrice': formatted_stop, 'price': formatted_limit
            }, response)
            
            return format_order_response(response)
            
        except Exception as e:
            self.logger.error(f"Error placing stop-limit order: {e}")
            raise
    
    def place_oco_order(self, symbol: str, side: str, quantity: str,
                       price: str, stop_price: str, stop_limit_price: str) -> Dict[str, Any]:
        """Place an OCO (One-Cancels-Other) order."""
        try:
            # Validate inputs
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            if not validate_side(side):
                raise ValueError(f"Invalid side: {side}")
            
            if not validate_quantity(quantity):
                raise ValueError(f"Invalid quantity: {quantity}")
            
            if not validate_price(price) or not validate_price(stop_price) or not validate_price(stop_limit_price):
                raise ValueError("Invalid price parameters")
            
            # Format inputs
            formatted_qty = format_quantity(quantity)
            formatted_price = format_price(price)
            formatted_stop = format_price(stop_price)
            formatted_stop_limit = format_price(stop_limit_price)
            
            # Place order
            self.logger.info(f"Placing OCO {side} order for {formatted_qty} {symbol}")
            self.logger.info(f"Price: {formatted_price}, Stop: {formatted_stop}, Stop Limit: {formatted_stop_limit}")
            
            # Simulate OCO order placement
            response = self._simulate_order_response('OCO', symbol, side, formatted_qty, formatted_price, formatted_stop)
            response['stopLimitPrice'] = formatted_stop_limit
            
            # Log the order
            self.logger.order_placed('OCO', symbol, formatted_qty)
            self.logger.api_call('futures_create_order', {
                'symbol': symbol, 'side': side, 'type': 'OCO',
                'quantity': formatted_qty, 'price': formatted_price, 'stopPrice': formatted_stop
            }, response)
            
            return format_order_response(response)
            
        except Exception as e:
            self.logger.error(f"Error placing OCO order: {e}")
            raise
    
    def cancel_order(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order."""
        try:
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            self.logger.info(f"Cancelling order {order_id} for {symbol}")
            
            # Check if order exists
            if order_id not in self.orders:
                raise ValueError(f"Order {order_id} not found")
            
            # Simulate order cancellation
            response = {
                'orderId': order_id,
                'symbol': symbol.upper(),
                'status': 'CANCELED',
                'time': int(time.time() * 1000)
            }
            
            # Remove from orders
            if order_id in self.orders:
                del self.orders[order_id]
            
            self.logger.info(f"Order {order_id} cancelled successfully")
            self.logger.api_call('futures_cancel_order', {
                'symbol': symbol, 'orderId': order_id
            }, response)
            
            return format_order_response(response)
            
        except Exception as e:
            self.logger.error(f"Error cancelling order: {e}")
            raise
    
    def get_order_status(self, symbol: str, order_id: str) -> Dict[str, Any]:
        """Get the status of an order."""
        try:
            if not validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")
            
            self.logger.info(f"Getting status for order {order_id} on {symbol}")
            
            # Check if order exists
            if order_id not in self.orders:
                raise ValueError(f"Order {order_id} not found")
            
            response = self.orders[order_id].copy()
            response['updateTime'] = int(time.time() * 1000)
            
            self.logger.info(f"Order {order_id}: {response.get('status', 'UNKNOWN')}")
            self.logger.api_call('futures_get_order', {
                'symbol': symbol, 'orderId': order_id
            }, response)
            
            return format_order_response(response)
            
        except Exception as e:
            self.logger.error(f"Error getting order status: {e}")
            raise
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all open orders."""
        try:
            self.logger.info("Getting open orders")
            
            # Filter orders by symbol if specified
            open_orders = []
            for order in self.orders.values():
                if symbol is None or order['symbol'] == symbol.upper():
                    if order['status'] in ['NEW', 'PARTIALLY_FILLED']:
                        open_orders.append(order)
            
            self.logger.info(f"Found {len(open_orders)} open orders")
            self.logger.api_call('futures_get_open_orders', {'symbol': symbol} if symbol else {}, open_orders)
            
            return [format_order_response(order) for order in open_orders]
            
        except Exception as e:
            self.logger.error(f"Error getting open orders: {e}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        try:
            response = self.client.futures_account()
            self.logger.api_call('futures_account', {}, response)
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting account info: {e}")
            raise
