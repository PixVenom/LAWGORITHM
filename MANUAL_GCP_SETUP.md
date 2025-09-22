# Manual Google Cloud Setup Guide

Since the automated script had some issues, here's a step-by-step manual setup:

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: `legal-doc-simplifier`
3. Note your Project ID (e.g., `lawgorithm-472819`)

## Step 2: Enable APIs

Run these commands one by one:

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable vision.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

## Step 3: Create Service Account

```bash
# Create service account
gcloud iam service-accounts create legal-doc-service \
    --description="Service account for Legal Document Simplifier" \
    --display-name="Legal Doc Service"

# Wait a moment for it to be created
sleep 5
```

## Step 4: Grant Permissions

```bash
# Grant AI Platform access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:legal-doc-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Grant Storage access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:legal-doc-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Grant Vision API access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:legal-doc-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/vision.user"

# Grant Translation API access
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:legal-doc-service@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/translate.user"
```

## Step 5: Create Storage Bucket

```bash
# Create bucket (replace with your project ID)
gsutil mb gs://legal-doc-simplifier-YOUR_PROJECT_ID
```

## Step 6: Create Service Account Key

```bash
# Create and download key
gcloud iam service-accounts keys create ./gcp-key.json \
    --iam-account=legal-doc-service@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

## Step 7: Create Environment File

Create `backend/.env` with your details:

```bash
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
GOOGLE_CLOUD_PROJECT_ID=YOUR_PROJECT_ID
GCP_BUCKET_NAME=legal-doc-simplifier-YOUR_PROJECT_ID
GCP_REGION=us-central1

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# OCR Configuration
USE_GOOGLE_VISION=True

# AI Model Configuration
USE_VERTEX_AI=True
VERTEX_AI_MODEL=text-bison@001
```

## Step 8: Install Dependencies and Run

```bash
cd backend
pip install -r requirements-cloud.txt
python main.py
```

## Troubleshooting

If you get permission errors:
1. Make sure you're logged in: `gcloud auth login`
2. Check your project: `gcloud config get-value project`
3. Verify APIs are enabled in the Google Cloud Console

If service account creation fails:
1. Try a different name: `legal-doc-service-2`
2. Check if the name already exists in your project
