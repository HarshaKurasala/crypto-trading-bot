CRYPTO TRADING BOT - VERCEL DEPLOYMENT GUIDE
============================================

Created: December 10, 2025
Status: Ready for Production

---

📋 TABLE OF CONTENTS
====================

1. Prerequisites
2. Step-by-Step Deployment
3. Configuration Files
4. Environment Variables
5. API Endpoints
6. Troubleshooting
7. Post-Deployment

---

🔧 PREREQUISITES
================

Before deploying to Vercel, ensure you have:

✓ Vercel Account
  - Sign up at https://vercel.com
  - Connect your GitHub account

✓ GitHub Repository
  - Your code must be pushed to GitHub
  - https://github.com/HarshaKurasala/crypto-trading-bot

✓ Git Installed
  - Already installed on your system

✓ Required Files
  - api/index.py (Vercel entry point)
  - vercel.json (Configuration)
  - requirements.txt (Dependencies)
  - .vercelignore (Files to ignore)

---

📦 INSTALLATION & SETUP
=======================

Step 1: Install Vercel CLI
---------------------------

Open PowerShell and run:

npm install -g vercel

Or if you prefer:

npm i -g vercel


Step 2: Login to Vercel
------------------------

vercel login

You'll be prompted to:
- Enter your email
- Verify your email
- Authorize GitHub access

Verify with:

vercel whoami


Step 3: Deploy Your Project
-----------------------------

Navigate to your project directory:

cd "c:\Users\Harsha Vardhan\Documents\HARSHA PROJECTS\crypto-trading-bot-main"

Deploy:

vercel

You'll be asked:
1. "Set up and deploy?" → y (yes)
2. "Which scope?" → Select your account
3. "Link to existing project?" → n (no, unless redeploying)
4. "Project name?" → crypto-trading-bot
5. "Detected root directory?" → ./ (current directory)
6. "Want to modify settings?" → n (no)


Step 4: Automatic Deployment
------------------------------

Future deployments happen automatically when you:
- Push to your GitHub main branch
- Vercel will detect changes and redeploy


---

📁 PROJECT STRUCTURE FOR VERCEL
================================

Your project should have this structure:

crypto-trading-bot/
├── api/
│   └── index.py              (← Vercel entry point)
├── frontend/
│   ├── index.html
│   ├── signin.html
│   ├── signup.html
│   ├── profile.html
│   ├── styles.css
│   ├── script.js
│   └── profile.js
├── bot/
│   ├── __init__.py
│   ├── basic_bot.py
│   ├── logger.py
│   ├── order_handler.py
│   └── utils.py
├── vercel.json              (← Configuration file)
├── .vercelignore            (← Ignore file)
├── requirements.txt         (← Python dependencies)
└── README.md


---

⚙️ CONFIGURATION FILES EXPLANATION
===================================

1. vercel.json
--------------

{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}

What it does:
• version: 2 - Use Vercel v2 format
• builds: Tell Vercel to build Python from api/index.py
• routes: Direct all requests to the Flask app
• /api/* routes go to index.py
• All other routes also go to index.py


2. .vercelignore
----------------

Lists files NOT to upload:
• .git, __pycache__, *.pyc
• node_modules, venv/, build/
• .env.local, logs, test files
• Reduces deployment size


3. requirements.txt
-------------------

Must contain all Python dependencies:

flask==2.3.3
flask-cors==4.0.0
requests==2.31.0
python-dotenv==1.0.0
colorama==0.4.6
tabulate==0.9.0

Install locally with:
pip install -r requirements.txt


4. api/index.py
---------------

Entry point for Vercel:
• Flask app initialization
• Route definitions
• API endpoints
• Static file serving


---

🌐 API ENDPOINTS
================

After deployment, all endpoints are available at:
https://your-project-name.vercel.app/api/

List of endpoints:

1. GET /api/status
   Returns: Connection status
   Response: {
     "connected": true,
     "timestamp": 1702000000000,
     "demo_mode": true
   }

2. GET /api/symbols
   Returns: Available trading symbols
   Response: {
     "symbols": ["BTCUSDT", "ETHUSDT", ...]
   }

3. GET /api/price/<symbol>
   Example: /api/price/BTCUSDT
   Returns: Current price and 24h stats
   Response: {
     "symbol": "BTCUSDT",
     "current_price": 52340.50,
     "high_24h": 53200.00,
     "low_24h": 50150.75,
     "price_change_percent_24h": 2.50
   }

4. GET /api/trades/<symbol>
   Example: /api/trades/BTCUSDT
   Returns: Recent trades
   Response: [
     {
       "id": "1",
       "symbol": "BTCUSDT",
       "type": "BUY",
       "quantity": 0.25,
       "price": 49500,
       "pnl": "+$150"
     }
   ]

5. GET /api/orders
   Query: ?symbol=BTCUSDT
   Returns: Open orders
   Response: [
     {
       "id": "1",
       "symbol": "BTCUSDT",
       "type": "LIMIT",
       "side": "BUY",
       "quantity": 0.5,
       "price": 49000,
       "status": "OPEN"
     }
   ]

6. GET /api/account
   Returns: Account information
   Response: {
     "balance": 10000.00,
     "available": 9500.00,
     "pnl": 500.00,
     "total_trades": 25
   }


---

🔐 ENVIRONMENT VARIABLES
=========================

If you need environment variables:

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Add your variables:

Examples:

Name: FLASK_ENV
Value: production

Name: API_KEY
Value: your-api-key-here

Access in Python:

import os
api_key = os.environ.get('API_KEY')


---

🚀 DEPLOYMENT STEPS SUMMARY
============================

1. Install Vercel CLI
   npm install -g vercel

2. Push code to GitHub
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main

3. Login to Vercel
   vercel login

4. Deploy
   vercel

5. Follow prompts
   - Select account
   - Confirm project name
   - Accept defaults

6. Get your URL
   https://crypto-trading-bot.vercel.app

7. Test the API
   curl https://crypto-trading-bot.vercel.app/api/status


---

🧪 TESTING AFTER DEPLOYMENT
=============================

Test your deployment:

1. Frontend Pages:
   https://crypto-trading-bot.vercel.app/
   https://crypto-trading-bot.vercel.app/signin
   https://crypto-trading-bot.vercel.app/signup
   https://crypto-trading-bot.vercel.app/profile

2. API Status:
   https://crypto-trading-bot.vercel.app/api/status

3. Price Endpoint:
   https://crypto-trading-bot.vercel.app/api/price/BTCUSDT

4. Orders Endpoint:
   https://crypto-trading-bot.vercel.app/api/orders?symbol=BTCUSDT

Use browser console or curl to test.


---

🔍 MONITORING & LOGS
====================

View deployment logs:

1. Vercel Dashboard
   https://vercel.com/dashboard

2. Select your project
3. Click "Deployments"
4. View build logs and errors

Monitor in real-time:
   vercel logs crypto-trading-bot


---

⚠️ TROUBLESHOOTING
==================

Issue: "No module named 'bot'"
Solution:
  • Make sure bot/ folder is in root directory
  • Check imports in api/index.py
  • Rebuild: vercel --prod

Issue: 502 Bad Gateway
Solution:
  • Check requirements.txt is complete
  • View logs: vercel logs
  • Check Python syntax errors
  • Rebuild: vercel --prod

Issue: Static files not serving
Solution:
  • Use full paths for HTML files
  • Check frontend/ folder is in root
  • Check routes in vercel.json
  • Verify api/index.py sends files correctly

Issue: CORS errors
Solution:
  • Check Flask-CORS is installed
  • Verify CORS(app) in api/index.py
  • Rebuild: vercel --prod

Issue: API endpoints 404
Solution:
  • Check endpoint spelling
  • Verify routes in api/index.py
  • Check URL format: /api/endpoint
  • Verify vercel.json routing rules


---

📝 COMMON COMMANDS
==================

Deploy:
  vercel

Production deploy:
  vercel --prod

View logs:
  vercel logs [project-name]

List projects:
  vercel projects

Remove project:
  vercel remove [project-name]

Check status:
  vercel whoami


---

🎯 NEXT STEPS
=============

After deployment:

1. Share your URL
   https://crypto-trading-bot.vercel.app

2. Update frontend URLs
   Change localhost:5000 to your Vercel URL in:
   • script.js (API calls)
   • profile.js (API calls)

3. Connect frontend to API
   Update fetch calls:
   
   FROM:
   fetch('/api/price/BTCUSDT')
   
   TO:
   fetch('https://crypto-trading-bot.vercel.app/api/price/BTCUSDT')

4. Set up database (optional)
   • MongoDB, PostgreSQL, or Firebase
   • Add connection string as environment variable

5. Implement real authentication
   • JWT tokens
   • Password hashing
   • Database integration

6. Add HTTPS
   • Automatically provided by Vercel

7. Set up custom domain (optional)
   • Vercel Dashboard → Settings → Domains


---

💡 TIPS & BEST PRACTICES
=========================

✓ Always test locally first
  npm install && vercel dev

✓ Use environment variables for secrets
  API keys, database URLs, etc.

✓ Monitor deployments
  Vercel Dashboard → Deployments

✓ Keep dependencies updated
  pip freeze > requirements.txt
  npm update

✓ Use .vercelignore to reduce size
  Smaller deployments = faster

✓ Enable auto-deployments
  Vercel auto-deploys on GitHub push

✓ Monitor cold starts
  First request may be slow
  Subsequent requests are fast

✓ Use Vercel Analytics
  Monitor performance and errors


---

📊 DEPLOYMENT CHECKLIST
=======================

Before deploying:
☐ Code pushed to GitHub
☐ vercel.json created
☐ api/index.py created
☐ .vercelignore created
☐ requirements.txt updated
☐ All imports work locally
☐ No console errors
☐ Frontend builds locally

During deployment:
☐ Vercel CLI installed
☐ Logged in to Vercel
☐ Deployment completes successfully
☐ No build errors
☐ No 502 errors

After deployment:
☐ Frontend loads at https://...
☐ API endpoints respond
☐ Pages load correctly
☐ No console errors
☐ Performance is acceptable


---

🏁 FINAL SUMMARY
================

Your Crypto Trading Bot is now:
✓ Deployed on Vercel
✓ Globally accessible
✓ Auto-scaling
✓ Always on HTTPS
✓ Auto-deployed on GitHub push
✓ Free tier available

Live URL:
https://crypto-trading-bot.vercel.app

API Base:
https://crypto-trading-bot.vercel.app/api

Next: Update frontend to use production API URL


---

STATUS: READY FOR VERCEL DEPLOYMENT ✓

All configuration files created.
Follow this guide to deploy to Vercel.

For more help: https://vercel.com/docs
