# 🚀 Crypto Trading Bot - Full Stack

A professional-grade cryptocurrency trading bot with a modern web interface and Python backend, deployed on Vercel. Features realistic market simulation with dynamic zigzag price movements and advanced trading capabilities.

**⚡ Quick Links**
- 🎯 **[Complete Documentation](README_COMPLETE.md)** - Full project explanation
- 🌐 **[Live Demo](https://crypto-trading-bot-frontend.vercel.app)** - Trading interface
- 📡 **[API Docs](docs/API.md)** - Backend endpoints
- 🚀 **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy your own

## 📋 Quick Start

### What This Bot Does ✨

✅ **Real-time Trading Charts** - Candlestick charts with 6 timeframes (1m, 5m, 15m, 1h, 4h, 1d)
✅ **Realistic Price Movements** - Zigzag patterns with sharp reversals and momentum
✅ **Order Management** - Market, Limit, Stop-Limit, and OCO orders
✅ **Simulated Trading** - Safe demo environment to learn and test strategies
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Real-time Updates** - Prices and charts update every 1-2 seconds
✅ **Professional UI** - Dark theme with cyan accents and glassmorphism

## 📦 Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript ES6+ | Interactive trading interface |
| **Charts** | Chart.js 4.4.0 | Candlestick visualization |
| **Backend** | Python 3.9+, Flask 2.3.3 | API server & price simulation |
| **Hosting** | Vercel | Serverless deployment |
| **Control** | GitHub | Version control & CI/CD |

## 🎯 Features at a Glance

### Trading Features
- 📊 **5 Crypto Symbols**: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, ADAUSDT
- 🔄 **Order Types**: Market, Limit, Stop-Limit, OCO
- 📈 **Order Management**: Place, cancel, track orders
- 💰 **Portfolio Tracking**: Live balance and position updates
- 📋 **Trade History**: View recent filled orders

### Chart Features
- 🎨 **6 Timeframes**: 1m, 5m, 15m, 1h, 4h, 1d
- 🌊 **Zigzag Motion**: Sharp reversals and realistic price swings
- 📊 **Market Regimes**: Auto-switching between trending, volatile, consolidating states
- ⚡ **Real-time Updates**: New candle every 1-2 seconds
- 🔄 **Timeframe-Specific**: Each timeframe has unique volatility and trend patterns

### Technical Analysis
- 📊 High/Low prices
- 📈 Volume information
- 💹 Price change percentages
- 🎯 Bid/Ask spreads
- ⏱️ Real-time timestamps

## 🚀 Getting Started

### Option 1: Use Live Demo

Visit the live application:
```
https://crypto-trading-bot-frontend.vercel.app
```

No installation needed! Start trading immediately.

### Option 2: Local Development

```bash
# Clone repository
git clone https://github.com/HarshaKurasala/crypto-trading-bot
cd crypto-trading-bot

# Frontend setup
cd frontend
python server.py
# Open http://localhost:5000

# Backend setup (in another terminal)
cd backend
pip install -r requirements.txt
python index.py
# Backend runs at http://localhost:5000/api
```

### Option 3: Deploy Your Own

```bash
# Push to GitHub
git push origin main

# Frontend: Deploy to Vercel
# - Connect GitHub repo
# - Select 'frontend' as root
# - Deploy

# Backend: Deploy to Vercel
# - New project with 'backend' root
# - Add environment variables
# - Deploy
```

## 📊 Chart Behaviors Explained

The chart creates realistic trading patterns based on timeframe:

| Timeframe | Volatility | Trend Persistence | Pattern |
|-----------|-----------|------------------|---------|
| **1m** | Very High | Low | Choppy zigzag, frequent reversals |
| **5m** | High | Moderate | Regular bouncing patterns |
| **15m** | Medium | Balanced | Natural wave motion |
| **1h** | Lower | High | Strong trending with few reversals |
| **4h** | Low | Very High | Stable long-term trends |
| **1d** | Very Low | Extreme | Smooth gradual movements |

**Market Regimes** change every 8-15 candles:
- 🔼 **Trending**: Strong directional movement
- 📦 **Consolidating**: Tight ranges, mean reversion
- ⚡ **Volatile**: Large swings, frequent reversals
- 🔄 **Recovery**: Counter-trend movement, gradual reversals

## 💱 Trading Simulation

### How It Works

1. **Realistic Prices**: Base prices for real cryptocurrencies
2. **Dynamic Updates**: Prices change realistically every second
3. **Order Execution**: Orders fill at market simulation prices
4. **Portfolio Tracking**: Balance updates based on orders

### Supported Symbols

```
BTCUSDT  → Bitcoin      Base: $52,340
ETHUSDT  → Ethereum     Base: $3,145
BNBUSDT  → BNB Coin     Base: $625
SOLUSDT  → Solana       Base: $185
ADAUSDT  → Cardano      Base: $1.02
```

## 🔌 API Reference

All communication with backend uses JSON REST API.

### Key Endpoints

```http
GET  /api/health           # Check backend status
GET  /api/price/:symbol    # Get current price
POST /api/orders           # Place new order
GET  /api/orders/:symbol   # Get open orders
DEL  /api/orders/:id       # Cancel order
GET  /api/trades/:symbol   # Get trade history
```

See **[API Docs](docs/API.md)** for complete reference.

## 📁 Project Structure

```
crypto-trading-bot/
├── frontend/              # Vanilla JS + HTML + CSS (no frameworks)
│   ├── index.html        # Main trading interface
│   ├── script.js         # Trading logic (1,241 lines)
│   ├── styles.css        # Styling (1,050 lines)
│   ├── signin.html       # Login page
│   ├── signup.html       # Registration page
│   └── server.py         # Dev server
│
├── backend/               # Python Flask API
│   ├── index.py          # Flask app (293 lines)
│   ├── requirements.txt   # Dependencies
│   └── vercel.json       # Deployment config
│
├── docs/                  # Documentation
│   ├── API.md            # API reference
│   └── DEPLOYMENT.md     # Deploy guide
│
└── README_COMPLETE.md    # Full documentation (this project)
```

## 🔧 Configuration

### Frontend

Edit `frontend/index.html`:
```html
<script>
  // Development
  window.BACKEND_URL = 'http://localhost:5000/api';
  
  // Production
  // window.BACKEND_URL = 'https://backend.vercel.app/api';
</script>
```

### Backend

Create `backend/.env`:
```env
FLASK_ENV=development
BOT_AVAILABLE=True
DEMO_MODE=True
```

## 📡 Real-Time Features

### Price Updates
- **Frequency**: Every 1 second
- **Fluctuation**: Realistic ±0.02%
- **Display**: Smooth animated transitions

### Chart Updates
- **Frequency**: Every 1-2 seconds (controlled)
- **Pattern**: Zigzag with sharp reversals
- **Data**: 60 candles shown (sliding window)

### Order Updates
- **Frequency**: Every 3 seconds
- **Display**: Live order book
- **Notifications**: Order fill alerts

## 🎓 Learning

This bot is perfect for:
- 📚 **Learning trading**: Safe simulation environment
- 💻 **Learning code**: Clean, well-documented code
- 🔧 **Learning deployment**: Complete Vercel setup
- 📊 **Learning charts**: Chart.js implementation examples

## 🤝 Contributing

Want to improve the bot?

```bash
# 1. Fork repository
git fork https://github.com/HarshaKurasala/crypto-trading-bot

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes
# ... edit files ...

# 4. Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# 5. Open Pull Request
```

## 📞 Support

- 📖 **See [Full Docs](README_COMPLETE.md)** for detailed information
- 🐛 **Report bugs** in Issues tab
- 💬 **Discuss features** in Discussions tab
- 📧 **Email**: support@example.com

## 📄 License

MIT License - See LICENSE file for details

## 🎉 Status

✅ **Production Ready** - Fully functional and deployed
✅ **Well Documented** - Comprehensive documentation included
✅ **Actively Maintained** - Regular updates and improvements
✅ **Community Welcome** - Contributions encouraged

## ✨ Features

### 🔹 Core Trading Features
- **Market Orders**: Execute immediate buy/sell orders at current market price
- **Limit Orders**: Place orders at specific price levels
- **Stop-Limit Orders**: Advanced orders with stop and limit prices
- **OCO Orders**: One-Cancels-Other orders for risk management
- **Order Management**: Cancel, track, and monitor order status

### 🔹 Market Data
- Simulated real-time price information
- Symbol information and trading rules
- Recent trades data simulation
- Kline/candlestick data for technical analysis
- Account balance and position tracking

### 🔹 Advanced Features
- **Comprehensive Logging**: All operations logged with timestamps
- **Input Validation**: Robust validation for all user inputs
- **Error Handling**: Graceful error handling with detailed messages
- **Demo Mode**: Safe simulation environment with realistic market data
- **Beautiful CLI**: Color-coded, user-friendly command-line interface

### 🔹 Safety Features
- **Demo Mode by Default**: Uses simulated trading for safe testing
- **Input Sanitization**: All inputs validated and formatted
- **Connection Testing**: Automatic connection verification
- **Position Management**: Tools to close all positions safely

## 🔧 Prerequisites

- Python 3.8 or higher
- No external API credentials required (demo mode)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crypto-trading-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **No API setup required**
   The bot operates in demo mode and doesn't require real API credentials.

## ⚙️ Configuration

### Demo Mode Setup

The bot automatically operates in demo mode with the following features:

1. **Simulated Market Data**
   - Realistic price movements for popular cryptocurrencies
   - Simulated trading volume and market activity
   - Historical data patterns for technical analysis

2. **Simulated Trading**
   - All orders are simulated and don't affect real markets
   - Realistic order execution and status updates
   - Account balance simulation with $10,000 starting balance

3. **No Configuration Required**
   - No API keys or secrets needed
   - No external dependencies on exchange APIs
   - Ready to use immediately after installation

## 🚀 Usage

### Command Line Interface

Run the main CLI application:
```bash
python cli/main.py
```

### CLI Menu Options

```
📊 MAIN MENU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 ORDER MANAGEMENT
  1.  Place Market Order
  2.  Place Limit Order
  3.  Place Stop-Limit Order
  4.  Place OCO Order
  5.  Cancel Order
  6.  Get Order Status
  7.  View Open Orders

🔹 MARKET DATA
  8.  Get Symbol Price
  9.  Get Symbol Info
  10. Get Recent Trades
  11. Get Kline Data

🔹 ACCOUNT & POSITIONS
  12. Get Account Info
  13. Get Balance
  14. Close All Positions
  15. Cancel All Orders

🔹 UTILITIES
  16. Test Connection
  17. View Logs
  0.  Exit
```

### Programmatic Usage

```python
from bot.basic_bot import BasicBot

# Initialize the bot
bot = BasicBot(api_key="your_key", api_secret="your_secret", testnet=True)

# Place a market order
result = bot.place_market_order("BTCUSDT", "BUY", "0.001")
print(f"Order placed: {result}")

# Get current price
price_info = bot.get_symbol_price("BTCUSDT")
print(f"Current BTC price: {price_info['current_price']}")

# Get account balance
balance = bot.get_balance("USDT")
print(f"USDT balance: {balance['available_balance']}")
```

## 📚 API Reference

### BasicBot Class

#### Core Methods

```python
# Order Placement
place_market_order(symbol: str, side: str, quantity: str) -> Dict
place_limit_order(symbol: str, side: str, quantity: str, price: str) -> Dict
place_stop_limit_order(symbol: str, side: str, quantity: str, stop_price: str, limit_price: str) -> Dict
place_oco_order(symbol: str, side: str, quantity: str, price: str, stop_price: str, stop_limit_price: str) -> Dict

# Order Management
cancel_order(symbol: str, order_id: str) -> Dict
get_order_status(symbol: str, order_id: str) -> Dict
get_open_orders(symbol: Optional[str] = None) -> List[Dict]

# Market Data
get_symbol_price(symbol: str) -> Dict
get_symbol_info(symbol: str) -> Dict
get_recent_trades(symbol: str, limit: int = 10) -> List[Dict]
get_klines(symbol: str, interval: str = '1h', limit: int = 100) -> List[Dict]

# Account Management
get_account_info() -> Dict
get_balance(asset: str = 'USDT') -> Dict
close_all_positions() -> Dict
cancel_all_orders(symbol: Optional[str] = None) -> Dict
```

#### Parameters

- **symbol**: Trading pair (e.g., "BTCUSDT", "ETHUSDT")
- **side**: Order side ("BUY" or "SELL")
- **quantity**: Order quantity (string format)
- **price**: Order price (string format)
- **stop_price**: Stop price for stop-limit orders
- **limit_price**: Limit price for limit orders
- **order_id**: Unique order identifier
- **interval**: Kline interval ("1m", "5m", "1h", "1d", etc.)
- **limit**: Number of records to retrieve

### Utility Functions

```python
# Validation
validate_symbol(symbol: str) -> bool
validate_quantity(quantity: str) -> bool
validate_price(price: str) -> bool
validate_order_type(order_type: str) -> bool
validate_side(side: str) -> bool

# Formatting
format_quantity(quantity: str, precision: int = 6) -> str
format_price(price: str, precision: int = 2) -> str
calculate_notional_value(quantity: str, price: str) -> Decimal

# Advanced
validate_stop_limit_params(stop_price: str, limit_price: str, side: str) -> bool
calculate_stop_price(entry_price: str, stop_percentage: float, side: str) -> str
```

## 🧪 Testing

Run the test suite:
```bash
python tests/test_orders.py
```

Or run with pytest:
```bash
pytest tests/ -v
```

### Test Coverage

- ✅ Input validation functions
- ✅ Order placement and management
- ✅ Market data retrieval
- ✅ Error handling
- ✅ Logger functionality
- ✅ Utility functions

## 📁 Project Structure

```
crypto-trading-bot/
├── bot/                          # Core bot modules
│   ├── __init__.py
│   ├── basic_bot.py             # Main bot class
│   ├── order_handler.py         # Order management
│   ├── logger.py                # Logging system
│   └── utils.py                 # Utility functions
├── cli/                         # Command-line interface
│   ├── __init__.py
│   └── main.py                  # CLI application
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_orders.py           # Test suite
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── bot.log                      # Application logs (auto-generated)
└── README.md                    # This file
```

## 🔒 Security Considerations

### API Key Security
- **Never commit API keys** to version control
- Use environment variables for sensitive data
- Regularly rotate API keys
- Use testnet for development and testing

### Trading Safety
- Start with small amounts on testnet
- Test all strategies thoroughly before live trading
- Monitor logs for any unexpected behavior
- Use stop-loss orders to limit potential losses

### Best Practices
- Always validate inputs before processing
- Implement proper error handling
- Log all trading activities
- Test thoroughly before live deployment

## 🚨 Important Notes

### Testnet vs Mainnet
- This bot is configured for **Binance Futures Testnet** by default
- Testnet provides free test USDT for practice
- Switch to mainnet only after thorough testing
- Mainnet trading involves real money and risks

### Risk Disclaimer
- Cryptocurrency trading involves significant risk
- Past performance does not guarantee future results
- Only trade with funds you can afford to lose
- This bot is for educational purposes

### Limitations
- Testnet has different liquidity than mainnet
- Some advanced features may not be available on testnet
- API rate limits apply to both testnet and mainnet
- Network connectivity issues may affect order execution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python tests/test_orders.py

# Run linting (if using flake8)
flake8 bot/ cli/ tests/

# Run type checking (if using mypy)
mypy bot/ cli/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the logs in `bot.log` for debugging information
- Review the Binance API documentation for API-specific questions

## 🙏 Acknowledgments

- [Binance API](https://binance-docs.github.io/apidocs/futures/en/) for the trading API
- [python-binance](https://github.com/sammchardy/python-binance) for the Python client
- [Colorama](https://github.com/tartley/colorama) for colored terminal output
- [Tabulate](https://github.com/astanin/python-tabulate) for formatted tables

---

**⚠️ Disclaimer**: This software is for educational purposes only. Cryptocurrency trading involves substantial risk of loss and is not suitable for all investors. The value of cryptocurrencies can go down as well as up, and you may lose some or all of your investment. Always do your own research and consider consulting with a financial advisor before making any investment decisions.
