"""
Crypto Trading Bot Package

A comprehensive Python-based cryptocurrency trading bot for Binance Futures Testnet.
"""

from .basic_bot import BasicBot
from .order_handler import OrderHandler
from .logger import BotLogger, logger
from .utils import (
    validate_symbol, validate_quantity, validate_price, validate_order_type,
    validate_side, format_quantity, format_price, calculate_notional_value,
    validate_stop_limit_params, calculate_stop_price, format_order_response,
    get_symbol_info, parse_time_in_force
)

__version__ = "1.0.0"
__author__ = "Harsha Vardhan"
__email__ = "harsha@example.com"

__all__ = [
    'BasicBot',
    'OrderHandler', 
    'BotLogger',
    'logger',
    'validate_symbol',
    'validate_quantity',
    'validate_price',
    'validate_order_type',
    'validate_side',
    'format_quantity',
    'format_price',
    'calculate_notional_value',
    'validate_stop_limit_params',
    'calculate_stop_price',
    'format_order_response',
    'get_symbol_info',
    'parse_time_in_force'
] 