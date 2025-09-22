#!/bin/bash

# Google Cloud Setup Script for Legal Document Simplifier
# Run this script after creating your Google Cloud project

echo "🚀 Setting up Google Cloud for Legal Document Simplifier..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI is not installed. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID from user
read -p "Enter your Google Cloud Project ID: " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID is required!"
    exit 1
fi

echo "📋 Setting up project: $PROJECT_ID"

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable vision.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Create service account
echo "👤 Creating service account..."
gcloud iam service-accounts create legal-doc-service \
    --description="Service account for Legal Document Simplifier" \
    --display-name="Legal Doc Service" \
    --project=$PROJECT_ID

# Wait for service account to be created
echo "⏳ Waiting for service account to be created..."
sleep 10

# Grant permissions
echo "🔐 Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/vision.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/translate.user"

# Create storage bucket
BUCKET_NAME="legal-doc-simplifier-$PROJECT_ID"
echo "🪣 Creating storage bucket: $BUCKET_NAME"
gsutil mb gs://$BUCKET_NAME

# Create service account key
echo "🔑 Creating service account key..."
gcloud iam service-accounts keys create ./gcp-key.json \
    --iam-account=legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com \
    --project=$PROJECT_ID

# Create .env file
echo "📝 Creating .env file..."
cat > backend/.env << EOF
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID
GCP_BUCKET_NAME=$BUCKET_NAME
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
EOF

echo "✅ Google Cloud setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your OpenAI API key to backend/.env (optional)"
echo "2. Run: cd backend && pip install -r requirements-cloud.txt"
echo "3. Run: python main.py"
echo ""
echo "🔗 Your project details:"
echo "   Project ID: $PROJECT_ID"
echo "   Bucket: $BUCKET_NAME"
echo "   Service Account: legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com"
echo ""
echo "⚠️  Keep your gcp-key.json file secure and never commit it to git!"
