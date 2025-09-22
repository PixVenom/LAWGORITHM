#!/bin/bash

# Cloud Run Deployment Script for Legal Document Simplifier
echo "🚀 Deploying to Google Cloud Run..."

# Get project ID
read -p "Enter your Google Cloud Project ID: " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID is required!"
    exit 1
fi

# Set project
gcloud config set project $PROJECT_ID

# Set region
REGION="us-central1"
SERVICE_NAME="legal-doc-simplifier"

echo "📋 Deploying to:"
echo "   Project: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Service: $SERVICE_NAME"

# Build and deploy to Cloud Run
echo "🔨 Building and deploying..."
gcloud run deploy $SERVICE_NAME \
    --source backend \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars "GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID" \
    --set-env-vars "GCP_REGION=$REGION" \
    --set-env-vars "USE_GOOGLE_VISION=True" \
    --set-env-vars "USE_VERTEX_AI=True"

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your app is available at:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"
echo ""
echo "📋 To update your frontend:"
echo "   Update REACT_APP_API_URL in frontend/vercel.json with the URL above"
