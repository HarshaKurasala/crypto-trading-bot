#  Crypto Trading Bot - Deployment Explanation

## Overview
This document explains how the **backend** and **frontend** of the Crypto Trading Bot are deployed on **Vercel**.

---

##  Architecture

The application follows a **single serverless function** architecture:

### Frontend Layer
- **Files**: rontend/index.html, signin.html, signup.html, profile.html, script.js, styles.css
- **Served By**: Flask's send_from_directory() in pi/index.py
- **Path Configuration**: FRONTEND_PATH = os.path.join(os.path.dirname(__file__), '..', 'frontend')

### Backend Layer
- **File**: pi/index.py (Serverless function)
- **Runtime**: Python 3.9+
- **Framework**: Flask
- **Endpoints**:
  - GET /  Serves index.html
  - GET /signin  Serves signin.html
  - GET /signup  Serves signup.html
  - GET /profile  Serves profile.html
  - GET /api/status  Bot status (JSON)
  - GET /api/symbols  Trading pairs (JSON)
  - GET /api/price/{symbol}  Crypto prices (JSON)
  - GET /api/orders  Trading orders (JSON)
  - GET /api/account  Account info (JSON)
  - GET /api/trades  Trading history (JSON)

---

##  How Backend is Deployed

### **1. Serverless Function Configuration**
File: ercel.json
\\\json
{
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
\\\

**What happens:**
- Vercel sees ercel.json configuration
- Identifies pi/index.py as the build source
- Uses @vercel/python runtime
- Routes ALL requests to pi/index.py

### **2. Flask App Setup**
File: pi/index.py (Lines 1-30)

\\\python
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

# Determine frontend path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
FRONTEND_PATH = os.path.join(PARENT_DIR, 'frontend')

# Create Flask app with static folder configuration
app = Flask(__name__, static_folder=FRONTEND_PATH, static_url_path='')
CORS(app)
\\\

**Why this works:**
- FRONTEND_PATH points to the frontend directory
- static_folder=FRONTEND_PATH tells Flask where to find files
- static_url_path='' makes them accessible at root URL

### **3. Route Handlers**
File: pi/index.py (Lines 40-80)

\\\python
@app.route('/')
def index():
    return send_from_directory(FRONTEND_PATH, 'index.html')

@app.route('/signin')
def signin():
    return send_from_directory(FRONTEND_PATH, 'signin.html')

@app.route('/api/status')
def get_status():
    return jsonify({
        'connected': BOT_AVAILABLE,
        'timestamp': int(time.time() * 1000),
        'demo_mode': True
    })
\\\

**How it works:**
1. User requests /  Flask matches first route
2. send_from_directory(FRONTEND_PATH, 'index.html') reads the file
3. File content sent to user's browser as HTML response

### **4. Deployment Flow**
`
1. Developer: git push origin main
   
2. GitHub: Triggers Vercel webhook
   
3. Vercel: Detects vercel.json
   
4. Vercel: Builds api/index.py using @vercel/python
   
5. Vercel: Installs dependencies from requirements.txt
   
6. Vercel: Creates serverless function
   
7. Vercel: Deploys to global edge network
   
8. App: Available at DEPLOYMENT_URL
`

---

##  How Frontend is Deployed

### **1. File Structure**
`
project/
 api/
    index.py                 (Serverless entry point)
 frontend/
    index.html               (Main dashboard HTML)
    signin.html              (Login page)
    signup.html              (Register page)
    profile.html             (User profile)
    script.js                (2000+ lines of logic)
    styles.css               (1000+ lines of styling)
`

### **2. Serving Mechanism**

Frontend files are **NOT** deployed as Vercel static files.

Instead, they are:
1. Kept in the rontend/ directory
2. Included with the serverless deployment
3. Served dynamically by Flask

**Request Flow:**
`
User Browser
     GET https://...vercel.app/
    
Vercel Serverless Platform
     Routes to api/index.py
    
Flask App (api/index.py)
     @app.route('/')
    
send_from_directory(FRONTEND_PATH, 'index.html')
    
Reads frontend/index.html from disk
    
Returns HTML to browser
    
Browser parses HTML
     Links script.js and styles.css
    
Loads CSS from /styles.css
Loads JS from /script.js
     Browser makes AJAX requests
    
Fetch /api/price/BTCUSDT
Fetch /api/orders
Fetch /api/status
    
Flask routes to @app.route('/api/*')
    
Returns JSON data
    
JavaScript updates DOM with data
    
User sees interactive dashboard
`

### **3. JavaScript Communication**

Example from rontend/script.js:

\\\javascript
async function updatePriceDisplay() {
    try {
        // Fetch from /api/price
        const response = await fetch('/api/price/BTCUSDT');
        const data = await response.json();
        
        // Update DOM
        document.querySelector('.price').textContent = 
            '\$' + data.current_price.toFixed(2);
    } catch (error) {
        console.error('Error loading price:', error);
    }
}

// Call every 2 seconds
setInterval(updatePriceDisplay, 2000);
\\\

**Why this works:**
- No CORS issues (same domain)
- Frontend and API on same serverless function
- Requests go through Vercel edge network
- Responses cached for performance

---

##  Project Structure

### **Essential Files**
| File | Purpose | Size |
|------|---------|------|
| pi/index.py | Serverless backend | ~240 lines |
| rontend/index.html | Dashboard | 403 lines |
| rontend/signin.html | Login page | 539 lines |
| rontend/signup.html | Register page | 736 lines |
| rontend/profile.html | User profile | 725 lines |
| rontend/script.js | All JS logic | 885 lines |
| rontend/styles.css | All styling | 1031 lines |
| ercel.json | Deployment config | 17 lines |
| equirements.txt | Python dependencies | 3 packages |

### **Removed Files (Cleaned)**
-  ot.log - Log files (production hazard)
-  __pycache__/ - Python cache (auto-generated)
-  .env.local - Local secrets (security risk)

---

##  Key Configuration Details

### **Path Resolution**
\\\python
# In api/index.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Result: /var/task/api (Vercel's function dir)

PARENT_DIR = os.path.dirname(CURRENT_DIR)
# Result: /var/task (Vercel's root)

FRONTEND_PATH = os.path.join(PARENT_DIR, 'frontend')
# Result: /var/task/frontend (where HTML files are)
\\\

### **CORS Configuration**
\\\python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enables cross-origin requests
\\\

This allows frontend (if on different domain) to access /api/* endpoints.

### **Static File Serving**
\\\python
app = Flask(__name__, 
    static_folder=FRONTEND_PATH,  # Where to find CSS/JS
    static_url_path=''             # Serve at root URL
)
\\\

When browser requests /styles.css:
1. Flask checks static_folder/styles.css
2. Finds rontend/styles.css
3. Sends file to browser

---

##  URL Structure

`
https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/

Pages:
  /                     Dashboard (index.html)
  /signin               Login (signin.html)
  /signup               Register (signup.html)
  /profile              Profile (profile.html)

API Endpoints:
  /api/status           {"connected": false, "demo_mode": true}
  /api/symbols          {"symbols": ["BTCUSDT", "ETHUSDT", ...]}
  /api/price/BTCUSDT    {"current_price": 52340.50, ...}
  /api/orders           {"orders": [...]}
  /api/account          {"balance": "10000.00", ...}
  /api/trades           {"trades": [...]}
`

---

##  Verification

### **Backend Working?**
\\\powershell
\https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/ = 'https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/api/status'
\{"available":9500.0,"balance":10000.0,"pnl":500.0,"pnl_percent":5.0,"total_trades":25,"win_rate":65.0}
 = Invoke-WebRequest \https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/ -UseBasicParsing
\{"available":9500.0,"balance":10000.0,"pnl":500.0,"pnl_percent":5.0,"total_trades":25,"win_rate":65.0}
.Content | ConvertFrom-Json
\\\

**Expected Output:**
\\\json
{
  "connected": false,
  "demo_mode": true,
  "timestamp": 1765357342799,
  "message": "Crypto Trading Bot API"
}
\\\

### **Frontend Working?**
`powershell
https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/ = 'https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/'
{"available":9500.0,"balance":10000.0,"pnl":500.0,"pnl_percent":5.0,"total_trades":25,"win_rate":65.0}
 = Invoke-WebRequest https://crypto-trading-bot-main-czkv9db08-harshas-projects-df72ee20.vercel.app/ -UseBasicParsing
{"available":9500.0,"balance":10000.0,"pnl":500.0,"pnl_percent":5.0,"total_trades":25,"win_rate":65.0}
.Content.Substring(0, 200)  # Check HTML content
`

**Expected:** HTML starting with <!DOCTYPE html>

---

##  Summary

**How It Works:**
1. **Single pi/index.py file** acts as the entire application
2. **Flask routes** determine what to return:
   - /, /signin, /signup, /profile  Return HTML pages
   - /api/*  Return JSON data
3. **Frontend files** stay in rontend/ directory
4. **send_from_directory()** dynamically reads and serves them
5. **Vercel serverless** runs the Flask app
6. **No static hosting** needed - everything through Flask

**Advantages:**
 Simple architecture  
 Single deployment  
 No CORS issues  
 Auto-scaling  
 Global CDN  
 Easy maintenance  

**Result:**
 Full-stack app deployed and working!

