# 📦 Deployment Guide - Vercel

This guide provides step-by-step instructions to deploy the Crypto Trading Bot to Vercel (frontend + backend).

## 📋 Prerequisites

- GitHub account with the repository
- Vercel account (free at https://vercel.com)
- Git installed locally

## 🎯 Architecture

The project uses a **separate deployment model**:
- **Frontend**: Static HTML/CSS/JS on Vercel (root directory)
- **Backend**: Python Flask API on Vercel (backend/ directory)

This allows independent scaling and updates.

## 🚀 Step-by-Step Deployment

### Phase 1: Frontend Deployment

#### Step 1: Deploy Frontend Project
1. Go to https://vercel.com/new
2. Click "Import Project"
3. Select GitHub and authorize Vercel
4. Search for `crypto-trading-bot`
5. Click "Import"

#### Step 2: Configure Frontend
1. **Project Name**: `crypto-trading-bot-frontend` (or your preference)
2. **Framework Preset**: `Other` (we use static HTML)
3. **Root Directory**: `./` (default, use root)
4. **Build Command**: Leave empty (no build needed)
5. **Output Directory**: Leave empty
6. **Environment Variables**: 
   - `REACT_APP_BACKEND_URL`: Leave empty for now (will update after backend deploys)

#### Step 3: Deploy
1. Click "Deploy"
2. Wait for deployment to complete (usually 1-2 minutes)
3. Your frontend URL will be shown (e.g., `https://crypto-trading-botfrontend.vercel.app`)
4. Click the URL to verify frontend loads

### Phase 2: Backend Deployment

#### Step 4: Deploy Backend Project
1. Go to https://vercel.com/new
2. Click "Import Project"
3. Search for `crypto-trading-bot` again
4. Click "Import"

#### Step 5: Configure Backend
1. **Project Name**: `crypto-trading-bot-backend` (different from frontend!)
2. **Framework Preset**: `Python`
3. **Root Directory**: `backend/` (THIS IS CRITICAL!)
   - Click "Edit" next to Root Directory
   - Change to `backend/`
   - Click "Save"
4. **Build Command**: Leave empty
5. **Install Command**: Leave empty (uses requirements.txt)
6. **Environment Variables**:
   ```
   FLASK_ENV=production
   PYTHONUNBUFFERED=1
   ```

#### Step 6: Deploy Backend
1. Click "Deploy"
2. Wait for deployment (may take 2-3 minutes)
3. Your backend URL will be shown (e.g., `https://crypto-trading-bot-backend.vercel.app`)
4. Test backend: Visit `https://crypto-trading-bot-backend.vercel.app/api/status`
   - Should see JSON response with `"connected": false`, `"demo_mode": true`

### Phase 3: Connect Frontend to Backend

#### Step 7: Update Frontend Environment Variables
1. Go to your Frontend project on Vercel
2. Go to "Settings" → "Environment Variables"
3. Add variable:
   - Name: `REACT_APP_BACKEND_URL`
   - Value: `https://crypto-trading-bot-backend.vercel.app` (your actual backend URL)
4. Click "Save"
5. Go to "Deployments"
6. Click the three-dot menu on latest deployment
7. Select "Redeploy"
8. Wait for redeployment

#### Step 8: Test Full Integration
1. Visit your frontend URL
2. Wait for dashboard to load
3. Check the connection indicator in top-left
4. Verify prices update (should show real demo data)
5. Open browser DevTools (F12) → Console
6. Should see no CORS errors

## 🔧 Configuration Details

### Frontend Environment Variables (.env.local)
```env
REACT_APP_BACKEND_URL=https://crypto-trading-bot-backend.vercel.app
REACT_APP_DEMO_MODE=true
REACT_APP_API_TIMEOUT=30000
```

### Backend Environment Variables (.env)
```env
FLASK_ENV=production
PYTHONUNBUFFERED=1
CORS_ORIGINS=*
```

## 🐛 Troubleshooting

### Issue: Frontend loads but shows "Disconnected"
**Cause**: Backend URL not set or incorrect
**Solution**:
1. Check `REACT_APP_BACKEND_URL` env variable in frontend project settings
2. Test backend URL directly in browser: `https://your-backend.vercel.app/api/status`
3. Redeploy frontend after updating env variable

### Issue: 404 Error when accessing backend
**Cause**: Root Directory not set to `backend/` for backend project
**Solution**:
1. Go to backend project settings
2. Check "Root Directory" is set to `backend/`
3. If not, change it and redeploy
4. Be sure this is a SEPARATE project from frontend

### Issue: CORS Error in browser console
**Cause**: Frontend and backend are not communicating
**Solution**:
1. Verify backend URL in frontend env variables
2. Check backend is returning CORS headers
3. Test: `curl -H "Origin: your-frontend.vercel.app" https://your-backend.vercel.app/api/status`

### Issue: High Latency/Slow Response
**Cause**: Cold start on serverless functions
**Solution**:
1. Normal for first request after deployment
2. Subsequent requests will be faster
3. Consider keeping frontend and backend in same region

## 📊 Expected Results

After successful deployment:

**Frontend Dashboard**:
- ✅ Loads instantly
- ✅ Shows trading interface with 4 pages
- ✅ Price data displays (BTC, ETH, BNB, SOL, ADA)
- ✅ "Connected" status shows in top-left
- ✅ Charts update every 5 seconds

**Backend API**:
- ✅ All endpoints respond with 200 OK
- ✅ Returns demo data for all symbols
- ✅ CORS headers present in responses

## 🔄 Redeployment

To redeploy after making changes:

1. **Push code to GitHub**:
   ```bash
   git add -A
   git commit -m "Your message"
   git push origin main
   ```

2. **Automatic Redeployment**:
   - Vercel automatically redeploys on push
   - Check "Deployments" tab in Vercel dashboard

3. **Manual Redeployment**:
   - Go to project → Deployments
   - Click three-dot menu on latest deployment
   - Select "Redeploy"

## 📱 Testing on Different Devices

1. **Desktop**: Visit your frontend URL directly
2. **Mobile**: Scan QR code from Vercel dashboard or visit URL
3. **Tablet**: Test responsive design (works on all sizes)

## 🚀 Advanced: Using Custom Domain

1. Go to Frontend project → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Same process for Backend if desired

## 📞 Support

**Common Issues Resources**:
- Vercel Docs: https://vercel.com/docs
- Python Deployment: https://vercel.com/docs/functions/serverless-functions/python
- CORS Issues: https://vercel.com/docs/serverless-functions/edge-functions#cors

---

**Version**: 1.0.0 | **Last Updated**: December 10, 2025
