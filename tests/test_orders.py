#!/usr/bin/env python3
"""
Unit tests for the Crypto Trading Bot
Tests for order handling, validation, and bot functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.basic_bot import BasicBot, DemoClient
from bot.order_handler import OrderHandler
from bot.utils import (
    validate_symbol, validate_quantity, validate_price, validate_order_type,
    validate_side, format_quantity, format_price, calculate_notional_value,
    validate_stop_limit_params, calculate_stop_price
)
from bot.logger import BotLogger


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_validate_symbol(self):
        """Test symbol validation."""
        # Valid symbols
        self.assertTrue(validate_symbol("BTCUSDT"))
        self.assertTrue(validate_symbol("ETHUSDT"))
        self.assertTrue(validate_symbol("ADAUSDT"))
        
        # Invalid symbols
        self.assertFalse(validate_symbol(""))
        self.assertFalse(validate_symbol("BTC"))
        self.assertFalse(validate_symbol("BTCUSD"))
        self.assertFalse(validate_symbol("btcusdt"))
        self.assertFalse(validate_symbol("123USDT"))
    
    def test_validate_quantity(self):
        """Test quantity validation."""
        # Valid quantities
        self.assertTrue(validate_quantity("1.0"))
        self.assertTrue(validate_quantity("0.001"))
        self.assertTrue(validate_quantity("100"))
        
        # Invalid quantities
        self.assertFalse(validate_quantity(""))
        self.assertFalse(validate_quantity("0"))
        self.assertFalse(validate_quantity("-1"))
        self.assertFalse(validate_quantity("abc"))
        self.assertFalse(validate_quantity("1.0.0"))
    
    def test_validate_price(self):
        """Test price validation."""
        # Valid prices
        self.assertTrue(validate_price("1.0"))
        self.assertTrue(validate_price("0.001"))
        self.assertTrue(validate_price("50000"))
        
        # Invalid prices
        self.assertFalse(validate_price(""))
        self.assertFalse(validate_price("0"))
        self.assertFalse(validate_price("-1"))
        self.assertFalse(validate_price("abc"))
        self.assertFalse(validate_price("1.0.0"))
    
    def test_validate_order_type(self):
        """Test order type validation."""
        # Valid order types
        self.assertTrue(validate_order_type("MARKET"))
        self.assertTrue(validate_order_type("LIMIT"))
        self.assertTrue(validate_order_type("STOP_LIMIT"))
        self.assertTrue(validate_order_type("OCO"))
        
        # Invalid order types
        self.assertFalse(validate_order_type(""))
        self.assertFalse(validate_order_type("INVALID"))
        self.assertFalse(validate_order_type("market"))
    
    def test_validate_side(self):
        """Test side validation."""
        # Valid sides
        self.assertTrue(validate_side("BUY"))
        self.assertTrue(validate_side("SELL"))
        
        # Invalid sides
        self.assertFalse(validate_side(""))
        self.assertFalse(validate_side("buy"))
        self.assertFalse(validate_side("INVALID"))
    
    def test_format_quantity(self):
        """Test quantity formatting."""
        self.assertEqual(format_quantity("1.123456789", 6), "1.123456")
        self.assertEqual(format_quantity("1.0", 2), "1.00")
        self.assertEqual(format_quantity("0.001", 3), "0.001")
    
    def test_format_price(self):
        """Test price formatting."""
        self.assertEqual(format_price("1.123456789", 2), "1.12")
        self.assertEqual(format_price("50000.0", 2), "50000.00")
        self.assertEqual(format_price("0.001", 4), "0.0010")
    
    def test_calculate_notional_value(self):
        """Test notional value calculation."""
        from decimal import Decimal
        self.assertEqual(calculate_notional_value("1.0", "50000"), Decimal("50000"))
        self.assertEqual(calculate_notional_value("0.5", "100"), Decimal("50"))
        self.assertEqual(calculate_notional_value("2.0", "25.5"), Decimal("51.0"))
    
    def test_validate_stop_limit_params(self):
        """Test stop-limit parameter validation."""
        # Valid for BUY orders (stop <= limit)
        self.assertTrue(validate_stop_limit_params("100", "110", "BUY"))
        self.assertTrue(validate_stop_limit_params("100", "100", "BUY"))
        
        # Valid for SELL orders (stop >= limit)
        self.assertTrue(validate_stop_limit_params("110", "100", "SELL"))
        self.assertTrue(validate_stop_limit_params("100", "100", "SELL"))
        
        # Invalid for BUY orders (stop > limit)
        self.assertFalse(validate_stop_limit_params("110", "100", "BUY"))
        
        # Invalid for SELL orders (stop < limit)
        self.assertFalse(validate_stop_limit_params("100", "110", "SELL"))
    
    def test_calculate_stop_price(self):
        """Test stop price calculation."""
        # BUY orders: stop price below entry
        self.assertEqual(calculate_stop_price("100", 10, "BUY"), "90.00")
        self.assertEqual(calculate_stop_price("1000", 5, "BUY"), "950.00")
        
        # SELL orders: stop price above entry
        self.assertEqual(calculate_stop_price("100", 10, "SELL"), "110.00")
        self.assertEqual(calculate_stop_price("1000", 5, "SELL"), "1050.00")


class TestOrderHandler(unittest.TestCase):
    """Test order handler functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = DemoClient()
        self.order_handler = OrderHandler(self.mock_client)
    
    def test_place_market_order_success(self):
        """Test successful market order placement."""
        # Test order placement
        result = self.order_handler.place_market_order("BTCUSDT", "BUY", "0.001")
        
        # Verify result
        self.assertIsNotNone(result['order_id'])
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'BUY')
        self.assertEqual(result['type'], 'MARKET')
        
        # Verify order was stored
        order_id = result['order_id']
        self.assertIn(order_id, self.order_handler.orders)
    
    def test_place_market_order_invalid_symbol(self):
        """Test market order with invalid symbol."""
        with self.assertRaises(ValueError):
            self.order_handler.place_market_order("INVALID", "BUY", "0.001")
    
    def test_place_market_order_invalid_side(self):
        """Test market order with invalid side."""
        with self.assertRaises(ValueError):
            self.order_handler.place_market_order("BTCUSDT", "INVALID", "0.001")
    
    def test_place_market_order_invalid_quantity(self):
        """Test market order with invalid quantity."""
        with self.assertRaises(ValueError):
            self.order_handler.place_market_order("BTCUSDT", "BUY", "0")
    
    def test_place_limit_order_success(self):
        """Test successful limit order placement."""
        # Test order placement
        result = self.order_handler.place_limit_order("BTCUSDT", "SELL", "0.001", "50000")
        
        # Verify result
        self.assertIsNotNone(result['order_id'])
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'SELL')
        self.assertEqual(result['type'], 'LIMIT')
        self.assertEqual(result['price'], '50000.00')
        
        # Verify order was stored
        order_id = result['order_id']
        self.assertIn(order_id, self.order_handler.orders)
    
    def test_place_stop_limit_order_success(self):
        """Test successful stop-limit order placement."""
        # Test order placement
        result = self.order_handler.place_stop_limit_order("BTCUSDT", "BUY", "0.001", "45000", "46000")
        
        # Verify result
        self.assertIsNotNone(result['order_id'])
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'BUY')
        self.assertEqual(result['type'], 'STOP_MARKET')
        
        # Verify order was stored
        order_id = result['order_id']
        self.assertIn(order_id, self.order_handler.orders)
    
    def test_place_stop_limit_order_invalid_params(self):
        """Test stop-limit order with invalid parameters."""
        # Invalid for BUY orders (stop > limit)
        with self.assertRaises(ValueError):
            self.order_handler.place_stop_limit_order("BTCUSDT", "BUY", "0.001", "46000", "45000")
    
    def test_cancel_order_success(self):
        """Test successful order cancellation."""
        # First place an order
        order_result = self.order_handler.place_market_order("BTCUSDT", "BUY", "0.001")
        order_id = order_result['order_id']
        
        # Test order cancellation
        result = self.order_handler.cancel_order("BTCUSDT", order_id)
        
        # Verify result
        self.assertEqual(result['order_id'], order_id)
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['status'], 'CANCELED')
        
        # Verify order was removed
        self.assertNotIn(order_id, self.order_handler.orders)
    
    def test_get_order_status_success(self):
        """Test successful order status retrieval."""
        # First place an order
        order_result = self.order_handler.place_market_order("BTCUSDT", "BUY", "0.001")
        order_id = order_result['order_id']
        
        # Test order status retrieval
        result = self.order_handler.get_order_status("BTCUSDT", order_id)
        
        # Verify result
        self.assertEqual(result['order_id'], order_id)
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertIsNotNone(result['status'])
    
    def test_get_open_orders_success(self):
        """Test successful open orders retrieval."""
        # Place some orders
        self.order_handler.place_limit_order("BTCUSDT", "BUY", "0.001", "50000")
        self.order_handler.place_limit_order("ETHUSDT", "SELL", "0.01", "3000")
        
        # Test open orders retrieval
        result = self.order_handler.get_open_orders()
        
        # Verify result
        self.assertGreaterEqual(len(result), 2)
        
        # Verify all orders are open
        for order in result:
            self.assertIn(order['status'], ['NEW', 'PARTIALLY_FILLED'])


class TestBasicBot(unittest.TestCase):
    """Test BasicBot functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bot = BasicBot()
    
    def test_get_symbol_price_success(self):
        """Test successful symbol price retrieval."""
        # Test price retrieval
        result = self.bot.get_symbol_price("BTCUSDT")
        
        # Verify result
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertIsNotNone(result['current_price'])
        self.assertIsNotNone(result['bid_price'])
        self.assertIsNotNone(result['ask_price'])
    
    def test_get_symbol_price_invalid_symbol(self):
        """Test price retrieval with invalid symbol."""
        with self.assertRaises(ValueError):
            self.bot.get_symbol_price("INVALID")
    
    def test_get_recent_trades_success(self):
        """Test successful recent trades retrieval."""
        # Test trades retrieval
        result = self.bot.get_recent_trades("BTCUSDT", 2)
        
        # Verify result
        self.assertEqual(len(result), 2)
        self.assertIsNotNone(result[0]['id'])
        self.assertIsNotNone(result[1]['id'])
    
    def test_get_klines_success(self):
        """Test successful klines retrieval."""
        # Test klines retrieval
        result = self.bot.get_klines("BTCUSDT", "1h", 2)
        
        # Verify result
        self.assertEqual(len(result), 2)
        self.assertIsNotNone(result[0][1])  # open price
        self.assertIsNotNone(result[0][2])  # high price
        self.assertIsNotNone(result[0][3])  # low price
        self.assertIsNotNone(result[0][4])  # close price
    
    def test_close_all_positions_success(self):
        """Test successful closing of all positions."""
        # Test closing all positions
        result = self.bot.close_all_positions()
        
        # Verify result
        self.assertIn('closed_positions', result)
        # In demo mode, there are no positions to close initially
        self.assertIsInstance(result['closed_positions'], list)


class TestLogger(unittest.TestCase):
    """Test logger functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.logger = BotLogger('test.log')
    
    def test_logger_initialization(self):
        """Test logger initialization."""
        self.assertIsNotNone(self.logger.logger)
        # The logger level might be different due to handler configuration
        self.assertIn(self.logger.logger.level, [10, 20])  # INFO or WARNING level
    
    def test_logger_methods(self):
        """Test logger methods."""
        # Test that methods don't raise exceptions
        try:
            self.logger.info("Test info message")
            self.logger.warning("Test warning message")
            self.logger.error("Test error message")
            self.logger.debug("Test debug message")
            self.logger.api_call("test_endpoint", {"param": "value"}, {"response": "data"})
            self.logger.order_placed("MARKET", "BTCUSDT", "0.001")
            self.logger.order_status("12345", "FILLED")
        except Exception as e:
            self.fail(f"Logger methods should not raise exceptions: {e}")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    
    # Add test cases
    test_suite.addTest(loader.loadTestsFromTestCase(TestUtils))
    test_suite.addTest(loader.loadTestsFromTestCase(TestOrderHandler))
    test_suite.addTest(loader.loadTestsFromTestCase(TestBasicBot))
    test_suite.addTest(loader.loadTestsFromTestCase(TestLogger))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
