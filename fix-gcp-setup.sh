#!/bin/bash

# Quick fix for Google Cloud setup issues
echo "🔧 Fixing Google Cloud setup..."

# Get project ID from user
read -p "Enter your Google Cloud Project ID (e.g., lawgorithm-472819): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID is required!"
    exit 1
fi

echo "📋 Fixing setup for project: $PROJECT_ID"

# Set project
gcloud config set project $PROJECT_ID

# Check if service account exists
echo "🔍 Checking if service account exists..."
if gcloud iam service-accounts describe legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com &> /dev/null; then
    echo "✅ Service account already exists"
else
    echo "👤 Creating service account..."
    gcloud iam service-accounts create legal-doc-service \
        --description="Service account for Legal Document Simplifier" \
        --display-name="Legal Doc Service"
    
    # Wait for creation
    sleep 5
fi

# Grant permissions with correct roles
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
if gsutil ls gs://$BUCKET_NAME &> /dev/null; then
    echo "✅ Bucket already exists"
else
    gsutil mb gs://$BUCKET_NAME
fi

# Create service account key
echo "🔑 Creating service account key..."
if [ -f "./gcp-key.json" ]; then
    echo "✅ Key file already exists"
else
    gcloud iam service-accounts keys create ./gcp-key.json \
        --iam-account=legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com
fi

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

echo "✅ Google Cloud setup fixed!"
echo ""
echo "📋 Your configuration:"
echo "   Project ID: $PROJECT_ID"
echo "   Bucket: $BUCKET_NAME"
echo "   Service Account: legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com"
echo ""
echo "🚀 Next steps:"
echo "1. cd backend"
echo "2. pip install -r requirements-cloud.txt"
echo "3. python main.py"
