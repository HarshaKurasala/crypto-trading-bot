#!/usr/bin/env python3
"""
Crypto Trading Bot CLI Interface
A command-line interface for the BasicBot trading system.
"""

import sys
import os
import argparse
from typing import Optional
from colorama import Fore, Style, init
from tabulate import tabulate

# Add the parent directory to the path to import bot modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.basic_bot import BasicBot
from bot.logger import logger
from bot.utils import (
    validate_symbol, validate_quantity, validate_price, validate_order_type,
    validate_side, format_quantity, format_price
)

# Initialize colorama
init(autoreset=True)

class TradingBotCLI:
    def __init__(self):
        """Initialize the CLI interface."""
        self.bot = None
        self.running = True
    
    def print_banner(self):
        """Print the application banner."""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}CRYPTO TRADING BOT CLI{Fore.CYAN}                    ║
║                        {Fore.GREEN}DEMO MODE - SIMULATED TRADING{Fore.CYAN}                        ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def print_menu(self):
        """Print the main menu options."""
        menu = f"""
{Fore.YELLOW}📊 MAIN MENU{Style.RESET_ALL}
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}

{Fore.GREEN}🔹 ORDER MANAGEMENT{Style.RESET_ALL}
  1.  Place Market Order
  2.  Place Limit Order
  3.  Place Stop-Limit Order
  4.  Place OCO Order
  5.  Cancel Order
  6.  Get Order Status
  7.  View Open Orders

{Fore.BLUE}🔹 MARKET DATA{Style.RESET_ALL}
  8.  Get Symbol Price
  9.  Get Symbol Info
  10. Get Recent Trades
  11. Get Kline Data

{Fore.MAGENTA}🔹 ACCOUNT & POSITIONS{Style.RESET_ALL}
  12. Get Account Info
  13. Get Balance
  14. Close All Positions
  15. Cancel All Orders

{Fore.RED}🔹 UTILITIES{Style.RESET_ALL}
  16. Test Connection
  17. View Logs
  0.  Exit

{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
        """
        print(menu)
    
    def initialize_bot(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """Initialize the trading bot."""
        try:
            self.bot = BasicBot(api_key=api_key, api_secret=api_secret, testnet=False)
            logger.info("Bot initialized successfully in DEMO mode")
            print(f"{Fore.GREEN}✅ Bot initialized in DEMO mode - All operations are simulated{Style.RESET_ALL}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            print(f"{Fore.RED}❌ Failed to initialize bot: {e}{Style.RESET_ALL}")
            return False
    
    def get_user_input(self, prompt: str, validator=None, default: str = "") -> str:
        """Get user input with optional validation."""
        while True:
            if default:
                user_input = input(f"{Fore.CYAN}{prompt} (default: {default}): {Style.RESET_ALL}").strip()
                if not user_input:
                    user_input = default
            else:
                user_input = input(f"{Fore.CYAN}{prompt}: {Style.RESET_ALL}").strip()
            
            if validator is None or validator(user_input):
                return user_input
            else:
                print(f"{Fore.RED}❌ Invalid input. Please try again.{Style.RESET_ALL}")
    
    def place_market_order(self):
        """Handle market order placement."""
        print(f"\n{Fore.GREEN}📈 PLACE MARKET ORDER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        side = self.get_user_input("Enter side (BUY/SELL)", validate_side).upper()
        quantity = self.get_user_input("Enter quantity", validate_quantity)
        
        try:
            result = self.bot.place_market_order(symbol, side, quantity)
            print(f"\n{Fore.GREEN}✅ Market order placed successfully!{Style.RESET_ALL}")
            self.display_order_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to place market order: {e}{Style.RESET_ALL}")
    
    def place_limit_order(self):
        """Handle limit order placement."""
        print(f"\n{Fore.GREEN}📈 PLACE LIMIT ORDER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        side = self.get_user_input("Enter side (BUY/SELL)", validate_side).upper()
        quantity = self.get_user_input("Enter quantity", validate_quantity)
        price = self.get_user_input("Enter price", validate_price)
        time_in_force = self.get_user_input("Enter time in force (GTC/IOC/FOK)", default="GTC").upper()
        
        try:
            result = self.bot.place_limit_order(symbol, side, quantity, price, time_in_force)
            print(f"\n{Fore.GREEN}✅ Limit order placed successfully!{Style.RESET_ALL}")
            self.display_order_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to place limit order: {e}{Style.RESET_ALL}")
    
    def place_stop_limit_order(self):
        """Handle stop-limit order placement."""
        print(f"\n{Fore.GREEN}📈 PLACE STOP-LIMIT ORDER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        side = self.get_user_input("Enter side (BUY/SELL)", validate_side).upper()
        quantity = self.get_user_input("Enter quantity", validate_quantity)
        stop_price = self.get_user_input("Enter stop price", validate_price)
        limit_price = self.get_user_input("Enter limit price", validate_price)
        time_in_force = self.get_user_input("Enter time in force (GTC/IOC/FOK)", default="GTC").upper()
        
        try:
            result = self.bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price, time_in_force)
            print(f"\n{Fore.GREEN}✅ Stop-limit order placed successfully!{Style.RESET_ALL}")
            self.display_order_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to place stop-limit order: {e}{Style.RESET_ALL}")
    
    def place_oco_order(self):
        """Handle OCO order placement."""
        print(f"\n{Fore.GREEN}📈 PLACE OCO ORDER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        side = self.get_user_input("Enter side (BUY/SELL)", validate_side).upper()
        quantity = self.get_user_input("Enter quantity", validate_quantity)
        price = self.get_user_input("Enter limit price", validate_price)
        stop_price = self.get_user_input("Enter stop price", validate_price)
        stop_limit_price = self.get_user_input("Enter stop limit price", validate_price)
        
        try:
            result = self.bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
            print(f"\n{Fore.GREEN}✅ OCO order placed successfully!{Style.RESET_ALL}")
            self.display_order_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to place OCO order: {e}{Style.RESET_ALL}")
    
    def cancel_order(self):
        """Handle order cancellation."""
        print(f"\n{Fore.RED}❌ CANCEL ORDER{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        order_id = self.get_user_input("Enter order ID")
        
        try:
            result = self.bot.cancel_order(symbol, order_id)
            print(f"\n{Fore.GREEN}✅ Order cancelled successfully!{Style.RESET_ALL}")
            self.display_order_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to cancel order: {e}{Style.RESET_ALL}")
    
    def get_order_status(self):
        """Handle order status retrieval."""
        print(f"\n{Fore.BLUE}📊 GET ORDER STATUS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        order_id = self.get_user_input("Enter order ID")
        
        try:
            result = self.bot.get_order_status(symbol, order_id)
            print(f"\n{Fore.GREEN}✅ Order status retrieved!{Style.RESET_ALL}")
            self.display_order_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get order status: {e}{Style.RESET_ALL}")
    
    def view_open_orders(self):
        """Handle open orders display."""
        print(f"\n{Fore.BLUE}📊 OPEN ORDERS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (optional, press Enter to skip)", default="")
        if not symbol:
            symbol = None
        
        try:
            orders = self.bot.get_open_orders(symbol)
            if orders:
                print(f"\n{Fore.GREEN}✅ Found {len(orders)} open orders:{Style.RESET_ALL}")
                self.display_orders_table(orders)
            else:
                print(f"\n{Fore.YELLOW}📭 No open orders found{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get open orders: {e}{Style.RESET_ALL}")
    
    def get_symbol_price(self):
        """Handle symbol price retrieval."""
        print(f"\n{Fore.BLUE}💰 GET SYMBOL PRICE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        
        try:
            result = self.bot.get_symbol_price(symbol)
            print(f"\n{Fore.GREEN}✅ Price data retrieved!{Style.RESET_ALL}")
            self.display_price_info(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get price: {e}{Style.RESET_ALL}")
    
    def get_symbol_info(self):
        """Handle symbol info retrieval."""
        print(f"\n{Fore.BLUE}ℹ️  GET SYMBOL INFO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        
        try:
            result = self.bot.get_symbol_info(symbol)
            if result:
                print(f"\n{Fore.GREEN}✅ Symbol info retrieved!{Style.RESET_ALL}")
                self.display_symbol_info(result)
            else:
                print(f"\n{Fore.YELLOW}⚠️  Symbol not found{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get symbol info: {e}{Style.RESET_ALL}")
    
    def get_recent_trades(self):
        """Handle recent trades retrieval."""
        print(f"\n{Fore.BLUE}📈 RECENT TRADES{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        limit = self.get_user_input("Enter number of trades (1-1000)", default="10")
        
        try:
            result = self.bot.get_recent_trades(symbol, int(limit))
            print(f"\n{Fore.GREEN}✅ Recent trades retrieved!{Style.RESET_ALL}")
            self.display_trades_table(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get recent trades: {e}{Style.RESET_ALL}")
    
    def get_klines(self):
        """Handle kline data retrieval."""
        print(f"\n{Fore.BLUE}📊 KLINE DATA{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (e.g., BTCUSDT)", validate_symbol)
        interval = self.get_user_input("Enter interval (1m/3m/5m/15m/30m/1h/2h/4h/6h/8h/12h/1d/3d/1w/1M)", default="1h")
        limit = self.get_user_input("Enter number of klines (1-1000)", default="100")
        
        try:
            result = self.bot.get_klines(symbol, interval, int(limit))
            print(f"\n{Fore.GREEN}✅ Kline data retrieved!{Style.RESET_ALL}")
            self.display_klines_table(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get kline data: {e}{Style.RESET_ALL}")
    
    def get_account_info(self):
        """Handle account info retrieval."""
        print(f"\n{Fore.MAGENTA}👤 ACCOUNT INFO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        try:
            result = self.bot.get_account_info()
            print(f"\n{Fore.GREEN}✅ Account info retrieved!{Style.RESET_ALL}")
            self.display_account_info(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get account info: {e}{Style.RESET_ALL}")
    
    def get_balance(self):
        """Handle balance retrieval."""
        print(f"\n{Fore.MAGENTA}💰 GET BALANCE{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        asset = self.get_user_input("Enter asset (e.g., USDT)", default="USDT")
        
        try:
            result = self.bot.get_balance(asset)
            if result:
                print(f"\n{Fore.GREEN}✅ Balance retrieved!{Style.RESET_ALL}")
                self.display_balance_info(result)
            else:
                print(f"\n{Fore.YELLOW}⚠️  Asset not found{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to get balance: {e}{Style.RESET_ALL}")
    
    def close_all_positions(self):
        """Handle closing all positions."""
        print(f"\n{Fore.RED}⚠️  CLOSE ALL POSITIONS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        confirm = self.get_user_input("Are you sure you want to close ALL positions? (yes/no)")
        if confirm.lower() != 'yes':
            print(f"{Fore.YELLOW}❌ Operation cancelled{Style.RESET_ALL}")
            return
        
        try:
            result = self.bot.close_all_positions()
            print(f"\n{Fore.GREEN}✅ All positions closed!{Style.RESET_ALL}")
            self.display_positions_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to close positions: {e}{Style.RESET_ALL}")
    
    def cancel_all_orders(self):
        """Handle cancelling all orders."""
        print(f"\n{Fore.RED}⚠️  CANCEL ALL ORDERS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        symbol = self.get_user_input("Enter symbol (optional, press Enter to cancel all)", default="")
        if not symbol:
            symbol = None
        
        confirm = self.get_user_input("Are you sure you want to cancel ALL orders? (yes/no)")
        if confirm.lower() != 'yes':
            print(f"{Fore.YELLOW}❌ Operation cancelled{Style.RESET_ALL}")
            return
        
        try:
            result = self.bot.cancel_all_orders(symbol)
            print(f"\n{Fore.GREEN}✅ All orders cancelled!{Style.RESET_ALL}")
            self.display_orders_result(result)
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to cancel orders: {e}{Style.RESET_ALL}")
    
    def test_connection(self):
        """Handle connection testing."""
        print(f"\n{Fore.BLUE}🔗 TEST CONNECTION{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        try:
            # Test connection by getting account info
            result = self.bot.get_account_info()
            print(f"\n{Fore.GREEN}✅ Connection test successful!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Account can trade: {result.get('canTrade', 'Unknown')}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Connection test failed: {e}{Style.RESET_ALL}")
    
    def view_logs(self):
        """Handle log viewing."""
        print(f"\n{Fore.BLUE}📋 VIEW LOGS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        
        try:
            with open('bot.log', 'r') as f:
                logs = f.readlines()
                if logs:
                    print(f"\n{Fore.GREEN}📋 Recent logs:{Style.RESET_ALL}")
                    # Show last 20 lines
                    for line in logs[-20:]:
                        print(line.strip())
                else:
                    print(f"\n{Fore.YELLOW}📭 No logs found{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"\n{Fore.YELLOW}📭 Log file not found{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}❌ Failed to read logs: {e}{Style.RESET_ALL}")
    
    def display_order_result(self, result):
        """Display order result in a formatted table."""
        if not result:
            print(f"{Fore.YELLOW}No result data{Style.RESET_ALL}")
            return
        
        table_data = []
        for key, value in result.items():
            table_data.append([key.replace('_', ' ').title(), value])
        
        print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))
    
    def display_orders_table(self, orders):
        """Display orders in a formatted table."""
        if not orders:
            print(f"{Fore.YELLOW}No orders to display{Style.RESET_ALL}")
            return
        
        table_data = []
        for order in orders:
            table_data.append([
                order.get('order_id', 'N/A'),
                order.get('symbol', 'N/A'),
                order.get('side', 'N/A'),
                order.get('type', 'N/A'),
                order.get('quantity', 'N/A'),
                order.get('price', 'N/A'),
                order.get('status', 'N/A')
            ])
        
        headers = ['Order ID', 'Symbol', 'Side', 'Type', 'Quantity', 'Price', 'Status']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    def display_price_info(self, price_info):
        """Display price information in a formatted table."""
        if not price_info:
            print(f"{Fore.YELLOW}No price data{Style.RESET_ALL}")
            return
        
        table_data = []
        for key, value in price_info.items():
            table_data.append([key.replace('_', ' ').title(), value])
        
        print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))
    
    def display_symbol_info(self, symbol_info):
        """Display symbol information in a formatted table."""
        if not symbol_info:
            print(f"{Fore.YELLOW}No symbol data{Style.RESET_ALL}")
            return
        
        table_data = []
        for key, value in symbol_info.items():
            if key != 'filters':  # Skip filters for cleaner display
                table_data.append([key.replace('_', ' ').title(), value])
        
        print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))
    
    def display_trades_table(self, trades):
        """Display trades in a formatted table."""
        if not trades:
            print(f"{Fore.YELLOW}No trades to display{Style.RESET_ALL}")
            return
        
        table_data = []
        for trade in trades[:10]:  # Show only first 10 trades
            table_data.append([
                trade.get('id', 'N/A'),
                trade.get('price', 'N/A'),
                trade.get('quantity', 'N/A'),
                trade.get('side', 'N/A'),
                trade.get('time', 'N/A')
            ])
        
        headers = ['ID', 'Price', 'Quantity', 'Side', 'Time']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    def display_klines_table(self, klines):
        """Display klines in a formatted table."""
        if not klines:
            print(f"{Fore.YELLOW}No kline data{Style.RESET_ALL}")
            return
        
        table_data = []
        for kline in klines[:10]:  # Show only first 10 klines
            table_data.append([
                kline.get('open_time', 'N/A'),
                kline.get('open', 'N/A'),
                kline.get('high', 'N/A'),
                kline.get('low', 'N/A'),
                kline.get('close', 'N/A'),
                kline.get('volume', 'N/A')
            ])
        
        headers = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    
    def display_account_info(self, account_info):
        """Display account information in a formatted table."""
        if not account_info:
            print(f"{Fore.YELLOW}No account data{Style.RESET_ALL}")
            return
        
        # Display basic account info
        basic_info = {
            'Can Trade': account_info.get('canTrade', 'N/A'),
            'Can Withdraw': account_info.get('canWithdraw', 'N/A'),
            'Can Deposit': account_info.get('canDeposit', 'N/A'),
            'Update Time': account_info.get('updateTime', 'N/A')
        }
        
        table_data = []
        for key, value in basic_info.items():
            table_data.append([key, value])
        
        print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))
    
    def display_balance_info(self, balance_info):
        """Display balance information in a formatted table."""
        if not balance_info:
            print(f"{Fore.YELLOW}No balance data{Style.RESET_ALL}")
            return
        
        table_data = []
        for key, value in balance_info.items():
            table_data.append([key.replace('_', ' ').title(), value])
        
        print(tabulate(table_data, headers=['Field', 'Value'], tablefmt='grid'))
    
    def display_positions_result(self, result):
        """Display positions result in a formatted table."""
        if not result:
            print(f"{Fore.YELLOW}No positions data{Style.RESET_ALL}")
            return
        
        closed_positions = result.get('closed_positions', [])
        if closed_positions:
            table_data = []
            for pos in closed_positions:
                table_data.append([
                    pos.get('symbol', 'N/A'),
                    pos.get('side', 'N/A'),
                    pos.get('quantity', 'N/A')
                ])
            
            headers = ['Symbol', 'Side', 'Quantity']
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
        else:
            print(f"{Fore.YELLOW}No positions were closed{Style.RESET_ALL}")
    
    def display_orders_result(self, result):
        """Display orders result in a formatted table."""
        if not result:
            print(f"{Fore.YELLOW}No orders data{Style.RESET_ALL}")
            return
        
        cancelled_orders = result.get('cancelled_orders', [])
        if cancelled_orders:
            table_data = []
            for order in cancelled_orders:
                table_data.append([
                    order.get('symbol', 'N/A'),
                    order.get('order_id', 'N/A')
                ])
            
            headers = ['Symbol', 'Order ID']
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
        else:
            print(f"{Fore.YELLOW}No orders were cancelled{Style.RESET_ALL}")
    
    def run(self):
        """Run the CLI interface."""
        self.print_banner()
        
        # Initialize bot
        if not self.initialize_bot():
            return
        
        # Main loop
        while self.running:
            try:
                self.print_menu()
                choice = input(f"\n{Fore.CYAN}Enter your choice (0-17): {Style.RESET_ALL}").strip()
                
                if choice == '0':
                    print(f"\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
                    self.running = False
                elif choice == '1':
                    self.place_market_order()
                elif choice == '2':
                    self.place_limit_order()
                elif choice == '3':
                    self.place_stop_limit_order()
                elif choice == '4':
                    self.place_oco_order()
                elif choice == '5':
                    self.cancel_order()
                elif choice == '6':
                    self.get_order_status()
                elif choice == '7':
                    self.view_open_orders()
                elif choice == '8':
                    self.get_symbol_price()
                elif choice == '9':
                    self.get_symbol_info()
                elif choice == '10':
                    self.get_recent_trades()
                elif choice == '11':
                    self.get_klines()
                elif choice == '12':
                    self.get_account_info()
                elif choice == '13':
                    self.get_balance()
                elif choice == '14':
                    self.close_all_positions()
                elif choice == '15':
                    self.cancel_all_orders()
                elif choice == '16':
                    self.test_connection()
                elif choice == '17':
                    self.view_logs()
                else:
                    print(f"\n{Fore.RED}❌ Invalid choice. Please enter a number between 0 and 17.{Style.RESET_ALL}")
                
                if self.running:
                    input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                    print("\n" + "="*80 + "\n")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}⚠️  Interrupted by user{Style.RESET_ALL}")
                self.running = False
            except Exception as e:
                print(f"\n{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
                logger.error(f"CLI error: {e}")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Crypto Trading Bot CLI')
    parser.add_argument('--api-key', help='Binance API key')
    parser.add_argument('--api-secret', help='Binance API secret')
    
    args = parser.parse_args()
    
    cli = TradingBotCLI()
    cli.run()

if __name__ == "__main__":
    main()
