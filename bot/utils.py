import re
import decimal
from decimal import Decimal, ROUND_DOWN
from typing import Optional, Dict, Any

def validate_symbol(symbol: str) -> bool:
    """Validate trading symbol format."""
    if not symbol:
        return False
    
    # Basic validation for common crypto pairs - must start with letter
    pattern = r'^[A-Z][A-Z0-9]*USDT$'
    return bool(re.match(pattern, symbol))

def validate_quantity(quantity: str) -> bool:
    """Validate quantity format."""
    if not quantity or not quantity.strip():
        return False
    try:
        qty = Decimal(quantity)
        return qty > 0
    except (ValueError, TypeError, decimal.InvalidOperation):
        return False

def validate_price(price: str) -> bool:
    """Validate price format."""
    if not price or not price.strip():
        return False
    try:
        price_decimal = Decimal(price)
        return price_decimal > 0
    except (ValueError, TypeError, decimal.InvalidOperation):
        return False

def format_quantity(quantity: str, precision: int = 6) -> str:
    """Format quantity to specified precision."""
    try:
        qty = Decimal(quantity)
        return str(qty.quantize(Decimal('0.' + '0' * precision), rounding=ROUND_DOWN))
    except (ValueError, TypeError):
        return quantity

def format_price(price: str, precision: int = 2) -> str:
    """Format price to specified precision."""
    try:
        price_decimal = Decimal(price)
        return str(price_decimal.quantize(Decimal('0.' + '0' * precision), rounding=ROUND_DOWN))
    except (ValueError, TypeError):
        return price

def calculate_notional_value(quantity: str, price: str) -> Decimal:
    """Calculate notional value of an order."""
    try:
        qty = Decimal(quantity)
        price_decimal = Decimal(price)
        return qty * price_decimal
    except (ValueError, TypeError):
        return Decimal('0')

def validate_order_type(order_type: str) -> bool:
    """Validate order type."""
    valid_types = ['MARKET', 'LIMIT', 'STOP_LIMIT', 'OCO']
    return order_type in valid_types

def validate_side(side: str) -> bool:
    """Validate order side."""
    valid_sides = ['BUY', 'SELL']
    return side in valid_sides

def parse_time_in_force(time_in_force: str) -> str:
    """Parse and validate time in force."""
    valid_tif = ['GTC', 'IOC', 'FOK', 'GTX']
    tif = time_in_force.upper()
    return tif if tif in valid_tif else 'GTC'

def format_order_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Format order response for better readability."""
    if not response:
        return {}
    
    formatted = {
        'order_id': response.get('orderId'),
        'symbol': response.get('symbol'),
        'side': response.get('side'),
        'type': response.get('type'),
        'quantity': response.get('origQty'),
        'price': response.get('price'),
        'status': response.get('status'),
        'time': response.get('time'),
        'update_time': response.get('updateTime')
    }
    
    return {k: v for k, v in formatted.items() if v is not None}

def get_symbol_info(symbol: str) -> Dict[str, Any]:
    """Get basic symbol information."""
    # This would typically come from exchange API
    # For now, return basic info
    return {
        'symbol': symbol.upper(),
        'base_asset': symbol.replace('USDT', ''),
        'quote_asset': 'USDT',
        'min_qty': '0.001',
        'max_qty': '1000000',
        'step_size': '0.001',
        'min_notional': '10'
    }

def calculate_stop_price(entry_price: str, stop_percentage: float, side: str) -> str:
    """Calculate stop price based on entry price and percentage."""
    try:
        entry = Decimal(entry_price)
        stop_percentage_decimal = Decimal(str(stop_percentage))
        
        if side.upper() == 'BUY':
            # For buy orders, stop price is below entry
            stop_price = entry * (Decimal('1') - stop_percentage_decimal / Decimal('100'))
        else:
            # For sell orders, stop price is above entry
            stop_price = entry * (Decimal('1') + stop_percentage_decimal / Decimal('100'))
        
        return format_price(str(stop_price), 2)
    except (ValueError, TypeError, decimal.InvalidOperation):
        return format_price(entry_price, 2)

def validate_stop_limit_params(stop_price: str, limit_price: str, side: str) -> bool:
    """Validate stop-limit order parameters."""
    try:
        stop = Decimal(stop_price)
        limit = Decimal(limit_price)
        
        if side.upper() == 'BUY':
            # For buy orders: stop_price <= limit_price
            return stop <= limit
        else:
            # For sell orders: stop_price >= limit_price
            return stop >= limit
    except (ValueError, TypeError, decimal.InvalidOperation):
        return False
