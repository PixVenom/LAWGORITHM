# 🔐 Google Cloud Authentication Setup

## Quick Fix for Credentials Error

The error "Your default credentials were not found" means you need to set up Google Cloud authentication.

## 🚀 Option 1: Automated Fix (Recommended)

Run the fix script:
```bash
./fix-credentials.sh
```

This will:
- Log you into Google Cloud
- Set up Application Default Credentials
- Create storage bucket and Firestore database
- Set up service account with proper permissions

## 🔧 Option 2: Manual Setup

### Step 1: Login to Google Cloud
```bash
gcloud auth login
```

### Step 2: Set Application Default Credentials
```bash
gcloud auth application-default login
```

### Step 3: Set Your Project
```bash
gcloud config set project YOUR_PROJECT_ID
```

### Step 4: Enable APIs
```bash
gcloud services enable storage.googleapis.com
gcloud services enable firestore.googleapis.com
```

### Step 5: Create Storage Bucket
```bash
gsutil mb gs://legal-doc-simplifier-YOUR_PROJECT_ID
```

### Step 6: Create Firestore Database
```bash
gcloud firestore databases create --region=us-central1
```

## 🎯 Option 3: Use Railway Instead (No Google Cloud Needed)

If you want to avoid Google Cloud setup entirely:

1. **Your Railway backend is already working!**
2. **Just deploy your frontend to Vercel**
3. **Use the existing Railway API**

## 🔍 Troubleshooting

### If you get "Project not found":
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Note the Project ID
4. Run the setup again

### If you get "Permission denied":
1. Make sure you're logged in: `gcloud auth list`
2. Check your project: `gcloud config get-value project`
3. Verify APIs are enabled in the Google Cloud Console

### If you get "Bucket already exists":
- This is normal! The script will use the existing bucket

## ✅ Verification

After setup, test your credentials:
```bash
# Test storage access
gsutil ls gs://your-bucket-name

# Test Firestore access
gcloud firestore databases list
```

## 🚀 Next Steps

Once authentication is working:

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements-datasets.txt
   ```

2. **Upload sample datasets:**
   ```bash
   python ../upload_sample_datasets.py
   ```

3. **Run enhanced backend:**
   ```bash
   python main_with_datasets.py
   ```

## 🎯 Alternative: Use Working Railway Backend

If Google Cloud setup is too complex:

- Your Railway backend at `https://legal-doc-backend-production.up.railway.app` is already working
- Just deploy your frontend to Vercel
- No Google Cloud authentication needed!

**Choose the option that works best for you!** 🚀
