@echo off
REM Vercel Deployment Quick Start Script
REM Run this script to deploy to Vercel

echo.
echo ========================================
echo Crypto Trading Bot - Vercel Deployment
echo ========================================
echo.

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: git is not installed!
    echo Please install git from https://git-scm.com/
    pause
    exit /b 1
)

echo [1/5] Installing Vercel CLI...
npm install -g vercel
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install Vercel CLI
    pause
    exit /b 1
)

echo.
echo [2/5] Verifying installation...
vercel --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Vercel CLI installation failed
    pause
    exit /b 1
)

echo.
echo [3/5] Committing changes to git...
git add .
git commit -m "Prepare for Vercel deployment: Add api/index.py, vercel.json, and deployment guide"
if %ERRORLEVEL% NEQ 0 (
    echo Note: git commit skipped (may be no changes)
)

echo.
echo [4/5] Pushing to GitHub...
git push origin main
if %ERRORLEVEL% NEQ 0 (
    echo Note: git push skipped (may be no changes)
)

echo.
echo [5/5] Starting Vercel deployment...
echo.
echo Follow the prompts:
echo - Sign in to Vercel (or create account)
echo - Select your GitHub account
echo - Confirm project name: crypto-trading-bot
echo - Accept default settings
echo.

vercel

echo.
echo ========================================
echo Deployment complete!
echo ========================================
echo.
echo Your app is deployed at:
echo https://crypto-trading-bot.vercel.app
echo.
echo Next steps:
echo 1. Visit the URL above to verify deployment
echo 2. Test API endpoints: /api/status, /api/price/BTCUSDT
echo 3. Update frontend fetch URLs to use production URL
echo.
pause
