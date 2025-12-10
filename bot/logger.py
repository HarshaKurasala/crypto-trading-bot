import logging
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

class BotLogger:
    def __init__(self, log_file='bot.log'):
        """Initialize the bot logger with file and console handlers."""
        self.logger = logging.getLogger('CryptoBot')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message with green color."""
        self.logger.info(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    
    def warning(self, message):
        """Log warning message with yellow color."""
        self.logger.warning(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def error(self, message):
        """Log error message with red color."""
        self.logger.error(f"{Fore.RED}{message}{Style.RESET_ALL}")
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
    
    def api_call(self, endpoint, params=None, response=None):
        """Log API call details."""
        log_msg = f"API Call: {endpoint}"
        if params:
            log_msg += f" | Params: {params}"
        if response:
            log_msg += f" | Response: {response}"
        self.info(log_msg)
    
    def order_placed(self, order_type, symbol, quantity, price=None):
        """Log order placement."""
        log_msg = f"Order Placed: {order_type} {quantity} {symbol}"
        if price:
            log_msg += f" @ {price}"
        self.info(log_msg)
    
    def order_status(self, order_id, status, details=None):
        """Log order status updates."""
        log_msg = f"Order {order_id}: {status}"
        if details:
            log_msg += f" | Details: {details}"
        self.info(log_msg)

# Global logger instance
logger = BotLogger()
