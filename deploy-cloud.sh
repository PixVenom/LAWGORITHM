#!/bin/bash

# Cloud Deployment Script for Legal Document Simplifier
# Supports Google Cloud, AWS, and Azure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CLOUD_PROVIDER="gcp"
PROJECT_ID=""
REGION="us-central1"
SERVICE_NAME="legal-doc-simplifier"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -p, --provider PROVIDER    Cloud provider (gcp, aws, azure) [default: gcp]"
    echo "  -i, --project-id ID        Project ID"
    echo "  -r, --region REGION        Deployment region [default: us-central1]"
    echo "  -s, --service-name NAME    Service name [default: legal-doc-simplifier]"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --provider gcp --project-id my-project"
    echo "  $0 --provider aws --region us-east-1"
    echo "  $0 --provider azure --region eastus"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--provider)
            CLOUD_PROVIDER="$2"
            shift 2
            ;;
        -i|--project-id)
            PROJECT_ID="$2"
            shift 2
            ;;
        -r|--region)
            REGION="$2"
            shift 2
            ;;
        -s|--service-name)
            SERVICE_NAME="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$PROJECT_ID" ]]; then
    print_error "Project ID is required. Use --project-id to specify it."
    exit 1
fi

print_status "Starting deployment to $CLOUD_PROVIDER..."
print_status "Project ID: $PROJECT_ID"
print_status "Region: $REGION"
print_status "Service Name: $SERVICE_NAME"

# Function to deploy to Google Cloud Platform
deploy_gcp() {
    print_status "Deploying to Google Cloud Platform..."
    
    # Check if gcloud is installed
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Set project
    gcloud config set project $PROJECT_ID
    
    # Enable required APIs
    print_status "Enabling required APIs..."
    gcloud services enable run.googleapis.com
    gcloud services enable vision.googleapis.com
    gcloud services enable translate.googleapis.com
    gcloud services enable aiplatform.googleapis.com
    gcloud services enable storage.googleapis.com
    
    # Create storage bucket if it doesn't exist
    BUCKET_NAME="${SERVICE_NAME}-documents-${PROJECT_ID}"
    print_status "Creating storage bucket: $BUCKET_NAME"
    gsutil mb gs://$BUCKET_NAME 2>/dev/null || print_warning "Bucket already exists or creation failed"
    
    # Deploy backend
    print_status "Deploying backend to Cloud Run..."
    gcloud run deploy ${SERVICE_NAME}-backend \
        --source backend \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars="GOOGLE_CLOUD_PROJECT_ID=$PROJECT_ID,GCP_BUCKET_NAME=$BUCKET_NAME,USE_CLOUD_OCR=true" \
        --memory=2Gi \
        --cpu=2 \
        --timeout=300 \
        --max-instances=10
    
    # Get backend URL
    BACKEND_URL=$(gcloud run services describe ${SERVICE_NAME}-backend --region=$REGION --format='value(status.url)')
    print_success "Backend deployed at: $BACKEND_URL"
    
    # Deploy frontend
    print_status "Deploying frontend to Cloud Run..."
    gcloud run deploy ${SERVICE_NAME}-frontend \
        --source frontend \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars="REACT_APP_API_URL=$BACKEND_URL" \
        --memory=1Gi \
        --cpu=1 \
        --timeout=60 \
        --max-instances=5
    
    # Get frontend URL
    FRONTEND_URL=$(gcloud run services describe ${SERVICE_NAME}-frontend --region=$REGION --format='value(status.url)')
    print_success "Frontend deployed at: $FRONTEND_URL"
    
    print_success "Deployment completed successfully!"
    print_status "Frontend URL: $FRONTEND_URL"
    print_status "Backend URL: $BACKEND_URL"
    print_status "Storage Bucket: gs://$BUCKET_NAME"
}

# Function to deploy to AWS
deploy_aws() {
    print_status "Deploying to AWS..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Create S3 bucket
    BUCKET_NAME="${SERVICE_NAME}-documents-${PROJECT_ID}"
    print_status "Creating S3 bucket: $BUCKET_NAME"
    aws s3 mb s3://$BUCKET_NAME --region $REGION 2>/dev/null || print_warning "Bucket already exists or creation failed"
    
    # Create ECR repository
    print_status "Creating ECR repository..."
    aws ecr create-repository --repository-name ${SERVICE_NAME}-backend --region $REGION 2>/dev/null || print_warning "Repository already exists"
    
    # Get ECR login token
    ECR_REGISTRY=$(aws ecr describe-repositories --repository-names ${SERVICE_NAME}-backend --region $REGION --query 'repositories[0].repositoryUri' --output text)
    
    # Build and push backend image
    print_status "Building and pushing backend image..."
    docker build -f backend/Dockerfile.cloud -t ${SERVICE_NAME}-backend ./backend
    docker tag ${SERVICE_NAME}-backend:latest $ECR_REGISTRY:latest
    aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
    docker push $ECR_REGISTRY:latest
    
    # Deploy with ECS (simplified - you may need to create task definition and service)
    print_status "Deploying to ECS..."
    print_warning "ECS deployment requires additional configuration. Please refer to the documentation."
    
    print_success "AWS deployment initiated!"
    print_status "ECR Registry: $ECR_REGISTRY"
    print_status "S3 Bucket: s3://$BUCKET_NAME"
}

# Function to deploy to Azure
deploy_azure() {
    print_status "Deploying to Azure..."
    
    # Check if Azure CLI is installed
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed. Please install it first."
        exit 1
    fi
    
    # Set subscription
    az account set --subscription $PROJECT_ID
    
    # Create resource group
    RESOURCE_GROUP="${SERVICE_NAME}-rg"
    print_status "Creating resource group: $RESOURCE_GROUP"
    az group create --name $RESOURCE_GROUP --location $REGION 2>/dev/null || print_warning "Resource group already exists"
    
    # Create storage account
    STORAGE_ACCOUNT="${SERVICE_NAME}storage$(date +%s)"
    print_status "Creating storage account: $STORAGE_ACCOUNT"
    az storage account create --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --location $REGION --sku Standard_LRS 2>/dev/null || print_warning "Storage account creation failed"
    
    # Create container registry
    ACR_NAME="${SERVICE_NAME}acr$(date +%s)"
    print_status "Creating container registry: $ACR_NAME"
    az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic 2>/dev/null || print_warning "ACR creation failed"
    
    # Build and push image
    print_status "Building and pushing image..."
    az acr build --registry $ACR_NAME --image ${SERVICE_NAME}-backend:latest ./backend
    
    # Deploy to Container Instances
    print_status "Deploying to Container Instances..."
    az container create \
        --resource-group $RESOURCE_GROUP \
        --name ${SERVICE_NAME}-backend \
        --image $ACR_NAME.azurecr.io/${SERVICE_NAME}-backend:latest \
        --cpu 2 \
        --memory 4 \
        --registry-login-server $ACR_NAME.azurecr.io \
        --registry-username $ACR_NAME \
        --registry-password $(az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv) \
        --ports 8080 \
        --environment-variables \
            AZURE_STORAGE_ACCOUNT=$STORAGE_ACCOUNT \
            AZURE_STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --query connectionString --output tsv) \
        --ip-address public
    
    print_success "Azure deployment completed!"
    print_status "Resource Group: $RESOURCE_GROUP"
    print_status "Storage Account: $STORAGE_ACCOUNT"
    print_status "Container Registry: $ACR_NAME.azurecr.io"
}

# Main deployment logic
case $CLOUD_PROVIDER in
    gcp|google)
        deploy_gcp
        ;;
    aws)
        deploy_aws
        ;;
    azure)
        deploy_azure
        ;;
    *)
        print_error "Unsupported cloud provider: $CLOUD_PROVIDER"
        print_error "Supported providers: gcp, aws, azure"
        exit 1
        ;;
esac

print_success "Deployment script completed!"
print_status "Don't forget to:"
print_status "1. Set up authentication credentials"
print_status "2. Configure environment variables"
print_status "3. Set up monitoring and logging"
print_status "4. Configure custom domain (optional)"
print_status "5. Set up SSL certificates (optional)"
