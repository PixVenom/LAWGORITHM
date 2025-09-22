#!/bin/bash

# Fix Google Cloud credentials setup
echo "🔐 Fixing Google Cloud credentials..."

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

echo "📋 Setting up credentials for project: $PROJECT_ID"

# Set project
gcloud config set project $PROJECT_ID

# Login to Google Cloud
echo "🔑 Logging in to Google Cloud..."
gcloud auth login

# Set application default credentials
echo "⚙️ Setting up Application Default Credentials..."
gcloud auth application-default login

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable storage.googleapis.com
gcloud services enable firestore.googleapis.com

# Create storage bucket
BUCKET_NAME="legal-doc-simplifier-$PROJECT_ID"
echo "🪣 Creating storage bucket: $BUCKET_NAME"
if gsutil ls gs://$BUCKET_NAME &> /dev/null; then
    echo "✅ Bucket already exists"
else
    gsutil mb gs://$BUCKET_NAME
fi

# Create Firestore database
echo "🔥 Setting up Firestore database..."
if gcloud firestore databases list --format="value(name)" | grep -q "projects/$PROJECT_ID/databases/(default)"; then
    echo "✅ Firestore database already exists"
else
    gcloud firestore databases create --region=us-central1
fi

# Create service account
echo "👤 Creating service account..."
if gcloud iam service-accounts describe legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com &> /dev/null; then
    echo "✅ Service account already exists"
else
    gcloud iam service-accounts create legal-doc-service \
        --description="Service account for Legal Document Simplifier" \
        --display-name="Legal Doc Service"
    
    # Wait for creation
    sleep 5
fi

# Grant permissions
echo "🔐 Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-doc-service@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/datastore.user"

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

# Dataset Configuration
USE_GCP_DATASETS=True
EOF

echo "✅ Google Cloud credentials setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. cd backend"
echo "2. pip install -r requirements-datasets.txt"
echo "3. python ../upload_sample_datasets.py"
echo "4. python main_with_datasets.py"
echo ""
echo "🔗 Your configuration:"
echo "   Project ID: $PROJECT_ID"
echo "   Bucket: $BUCKET_NAME"
echo "   Firestore: Enabled"
echo "   Credentials: Application Default Credentials + Service Account Key"
