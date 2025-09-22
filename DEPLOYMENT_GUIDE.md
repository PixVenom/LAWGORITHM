# 🚀 Deployment Guide - Legal Document Simplifier

## Current Status: ✅ Working Railway Deployment

Your app is already deployed and working! Here's how to use it:

### Backend (Railway) - ✅ WORKING
- **URL**: `https://legal-doc-backend-production.up.railway.app`
- **Status**: Deployed and running
- **Features**: Mock API responses for demo

### Frontend (Vercel) - Ready to Deploy

1. **Go to [Vercel](https://vercel.com)**
2. **Sign up with GitHub**
3. **Import Repository**: `PixVenom/LAWGORITHM`
4. **Deploy**: Vercel will automatically use your `frontend/vercel.json` config

## 🎯 Quick Demo Setup

### Option 1: Use Current Railway Backend (Recommended)
Your Railway backend is already working with mock responses. Just deploy the frontend to Vercel and you're done!

### Option 2: Add Google Cloud Features (Advanced)
If you want real AI features:

1. **Run the fix script:**
   ```bash
   ./fix-gcp-setup.sh
   ```

2. **Install cloud dependencies:**
   ```bash
   cd backend
   pip install -r requirements-cloud.txt
   ```

3. **Deploy to Cloud Run:**
   ```bash
   ./deploy-cloudrun.sh
   ```

## 🔧 Troubleshooting Cloud Run

If Cloud Run deployment fails:

### Common Issues:
1. **Build timeout** - Use minimal requirements
2. **Memory issues** - Increase memory allocation
3. **Python version** - Use Python 3.11

### Quick Fix:
```bash
# Use the minimal deployment
gcloud run deploy legal-doc-simplifier \
    --source backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --timeout 600
```

## 📱 Frontend Configuration

Your `frontend/vercel.json` is already configured with:
```json
{
  "env": {
    "REACT_APP_API_URL": "https://legal-doc-backend-production.up.railway.app/"
  }
}
```

## 🎉 Demo Features

Your deployed app includes:
- ✅ Document upload with mock OCR
- ✅ AI summaries (ELI5, Plain, Detailed)
- ✅ Risk assessment with color coding
- ✅ Interactive chatbot
- ✅ Modern Material UI design
- ✅ Responsive layout

## 🚀 Next Steps

1. **Deploy frontend to Vercel** (5 minutes)
2. **Test the full stack** (2 minutes)
3. **Ready for presentation!** 🎯

The Railway backend is already working perfectly for your demo!
