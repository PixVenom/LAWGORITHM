# Cloud Integration Guide for Legal Document Simplifier

This guide covers various cloud integration options to enhance your Legal Document Simplifier with scalable, production-ready cloud services.

## 🌐 Cloud Integration Options

### 1. **Google Cloud Platform (GCP) - Recommended**

#### Services to Integrate:
- **Cloud Run** - Serverless container deployment
- **Cloud Storage** - Document storage and retrieval
- **Vision API** - Enhanced OCR capabilities
- **Translation API** - Multi-language support
- **Vertex AI** - Advanced AI/ML models
- **Cloud SQL** - Database for user data
- **Cloud CDN** - Fast content delivery

#### Implementation Steps:

##### A. Enhanced OCR with Google Vision API
```python
# backend/services/cloud_ocr_service.py
from google.cloud import vision
from google.cloud import storage
import os

class CloudOCRService:
    def __init__(self):
        self.vision_client = vision.ImageAnnotatorClient()
        self.storage_client = storage.Client()
        self.bucket_name = os.getenv('GCP_BUCKET_NAME')
    
    async def process_document_cloud(self, file_path: str, user_id: str):
        # Upload to Cloud Storage
        blob_name = f"documents/{user_id}/{os.path.basename(file_path)}"
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        
        with open(file_path, 'rb') as file:
            blob.upload_from_file(file)
        
        # Process with Vision API
        image = vision.Image()
        image.source.image_uri = f"gs://{self.bucket_name}/{blob_name}"
        
        response = self.vision_client.document_text_detection(image=image)
        
        return {
            'text': response.full_text_annotation.text,
            'confidence': response.full_text_annotation.pages[0].confidence,
            'cloud_url': f"gs://{self.bucket_name}/{blob_name}"
        }
```

##### B. Cloud Storage Integration
```python
# backend/services/cloud_storage_service.py
from google.cloud import storage
import uuid
from datetime import datetime

class CloudStorageService:
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = os.getenv('GCP_BUCKET_NAME')
    
    async def upload_document(self, file_content: bytes, filename: str, user_id: str):
        # Generate unique filename
        file_id = str(uuid.uuid4())
        extension = filename.split('.')[-1]
        blob_name = f"documents/{user_id}/{file_id}.{extension}"
        
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        
        blob.upload_from_string(file_content)
        
        return {
            'file_id': file_id,
            'cloud_url': f"gs://{self.bucket_name}/{blob_name}",
            'public_url': blob.public_url,
            'uploaded_at': datetime.utcnow().isoformat()
        }
    
    async def get_document(self, file_id: str, user_id: str):
        blob_name = f"documents/{user_id}/{file_id}"
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        
        return blob.download_as_bytes()
```

##### C. Vertex AI Integration
```python
# backend/services/cloud_ai_service.py
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel

class CloudAIService:
    def __init__(self):
        vertexai.init(project=os.getenv('GCP_PROJECT_ID'))
        self.model = TextGenerationModel.from_pretrained("text-bison@001")
    
    async def generate_legal_summary(self, text: str, summary_type: str):
        if summary_type == "eli5":
            prompt = f"""
            Explain this legal document like I'm 5 years old. Use simple words and analogies.
            Focus on what the person can and cannot do, and what happens if they break the rules.
            
            Document: {text}
            """
        elif summary_type == "plain":
            prompt = f"""
            Summarize this legal document in plain, everyday language. Remove legal jargon.
            
            Document: {text}
            """
        else:
            prompt = f"""
            Provide a comprehensive summary of this legal document with all key details.
            
            Document: {text}
            """
        
        response = self.model.predict(
            prompt,
            max_output_tokens=1024,
            temperature=0.7
        )
        
        return response.text
```

### 2. **AWS Integration**

#### Services to Integrate:
- **Lambda** - Serverless functions
- **S3** - Document storage
- **Textract** - OCR service
- **Comprehend** - NLP and language detection
- **Bedrock** - AI/ML models
- **API Gateway** - API management
- **CloudFront** - CDN

#### Implementation:
```python
# backend/services/aws_service.py
import boto3
from botocore.exceptions import ClientError

class AWSService:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.textract_client = boto3.client('textract')
        self.comprehend_client = boto3.client('comprehend')
        self.bedrock_client = boto3.client('bedrock-runtime')
        self.bucket_name = os.getenv('AWS_S3_BUCKET')
    
    async def process_document_aws(self, file_path: str):
        # Upload to S3
        file_key = f"documents/{uuid.uuid4()}"
        self.s3_client.upload_file(file_path, self.bucket_name, file_key)
        
        # Process with Textract
        response = self.textract_client.detect_document_text(
            Document={'S3Object': {'Bucket': self.bucket_name, 'Name': file_key}}
        )
        
        # Extract text
        text = ""
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                text += block['Text'] + "\n"
        
        # Detect language with Comprehend
        lang_response = self.comprehend_client.detect_dominant_language(Text=text)
        language = lang_response['Languages'][0]['LanguageCode']
        
        return {
            'text': text,
            'language': language,
            's3_key': file_key,
            's3_url': f"s3://{self.bucket_name}/{file_key}"
        }
```

### 3. **Azure Integration**

#### Services to Integrate:
- **Azure Functions** - Serverless compute
- **Blob Storage** - Document storage
- **Computer Vision** - OCR capabilities
- **Translator** - Language services
- **OpenAI Service** - AI models
- **Application Insights** - Monitoring

#### Implementation:
```python
# backend/services/azure_service.py
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import requests

class AzureService:
    def __init__(self):
        self.blob_service = BlobServiceClient.from_connection_string(
            os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        )
        self.vision_client = ComputerVisionClient(
            endpoint=os.getenv('AZURE_VISION_ENDPOINT'),
            credentials=os.getenv('AZURE_VISION_KEY')
        )
    
    async def process_document_azure(self, file_path: str):
        # Upload to Blob Storage
        container_name = "documents"
        blob_name = f"{uuid.uuid4()}"
        
        with open(file_path, 'rb') as data:
            self.blob_service.upload_blob(
                container=container_name,
                name=blob_name,
                data=data
            )
        
        # Process with Computer Vision
        with open(file_path, 'rb') as image_stream:
            read_response = self.vision_client.read_in_stream(
                image_stream, raw=True
            )
        
        # Get results
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        
        while True:
            read_result = self.vision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
        
        # Extract text
        text = ""
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    text += line.text + "\n"
        
        return {
            'text': text,
            'blob_url': f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}.blob.core.windows.net/{container_name}/{blob_name}",
            'confidence': 0.95  # Azure doesn't provide confidence scores
        }
```

## 🚀 Deployment Strategies

### 1. **Google Cloud Run Deployment**

#### Dockerfile Updates:
```dockerfile
# backend/Dockerfile.cloud
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV PORT=8080
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# Expose port
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

#### Deployment Commands:
```bash
# Build and deploy to Cloud Run
gcloud run deploy legal-doc-backend \
  --source backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT_ID=your-project-id"

# Deploy frontend to Cloud Run
gcloud run deploy legal-doc-frontend \
  --source frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 2. **AWS ECS/Fargate Deployment**

#### Task Definition:
```json
{
  "family": "legal-doc-simplifier",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/legal-doc-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "AWS_DEFAULT_REGION",
          "value": "us-east-1"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/legal-doc-simplifier",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### 3. **Azure Container Instances**

#### Deployment Template:
```yaml
# azure-deployment.yaml
apiVersion: 2018-10-01
location: eastus
name: legal-doc-simplifier
properties:
  containers:
  - name: backend
    properties:
      image: your-registry.azurecr.io/legal-doc-backend:latest
      resources:
        requests:
          cpu: 1
          memoryInGb: 2
      ports:
      - port: 8000
        protocol: TCP
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 8000
  imageRegistryCredentials:
  - server: your-registry.azurecr.io
    username: your-username
    password: your-password
```

## 🔧 Configuration Updates

### Environment Variables for Cloud:
```bash
# .env.cloud
# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GCP_BUCKET_NAME=legal-docs-bucket
USE_CLOUD_OCR=true

# AWS
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=legal-docs-bucket
AWS_REGION=us-east-1

# Azure
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_VISION_ENDPOINT=your-vision-endpoint
AZURE_VISION_KEY=your-vision-key

# Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Redis (for caching)
REDIS_URL=redis://host:port
```

### Updated Requirements:
```txt
# backend/requirements-cloud.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0

# Google Cloud
google-cloud-vision==3.4.4
google-cloud-translate==3.11.1
google-cloud-aiplatform==1.38.1
google-cloud-storage==2.10.0

# AWS
boto3==1.34.0
botocore==1.34.0

# Azure
azure-storage-blob==12.19.0
azure-cognitiveservices-vision-computervision==0.9.0

# Database
sqlalchemy==2.0.23
alembic==1.13.1
psycopg2-binary==2.9.9

# Caching
redis==5.0.1

# Monitoring
opentelemetry-api==1.21.0
opentelemetry-sdk==1.21.0
opentelemetry-instrumentation-fastapi==0.42b0
```

## 📊 Monitoring and Logging

### 1. **Google Cloud Monitoring**
```python
# backend/services/monitoring_service.py
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import query
import time

class CloudMonitoringService:
    def __init__(self):
        self.client = monitoring_v3.MetricServiceClient()
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    
    def log_document_processed(self, user_id: str, processing_time: float):
        series = monitoring_v3.TimeSeries()
        series.metric.type = "custom.googleapis.com/legal_doc/processing_time"
        series.resource.type = "global"
        
        point = monitoring_v3.Point()
        point.value.double_value = processing_time
        point.interval.end_time.seconds = int(time.time())
        series.points = [point]
        
        self.client.create_time_series(
            name=f"projects/{self.project_id}",
            time_series=[series]
        )
```

### 2. **AWS CloudWatch**
```python
# backend/services/aws_monitoring.py
import boto3
import json

class AWSMonitoringService:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
    
    def log_metric(self, metric_name: str, value: float, unit: str = 'Count'):
        self.cloudwatch.put_metric_data(
            Namespace='LegalDocSimplifier',
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit,
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
```

## 🔐 Security Enhancements

### 1. **Authentication & Authorization**
```python
# backend/services/auth_service.py
from google.oauth2 import service_account
from google.auth.transport import requests
import jwt

class CloudAuthService:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        )
    
    def verify_token(self, token: str):
        try:
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded
        except jwt.InvalidTokenError:
            return None
    
    def generate_signed_url(self, blob_name: str, expiration_minutes: int = 60):
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(os.getenv('GCP_BUCKET_NAME'))
        blob = bucket.blob(blob_name)
        
        return blob.generate_signed_url(
            expiration=datetime.utcnow() + timedelta(minutes=expiration_minutes),
            method='GET'
        )
```

### 2. **Data Encryption**
```python
# backend/services/encryption_service.py
from cryptography.fernet import Fernet
import base64

class EncryptionService:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher = Fernet(self.key)
    
    def encrypt_document(self, content: bytes) -> bytes:
        return self.cipher.encrypt(content)
    
    def decrypt_document(self, encrypted_content: bytes) -> bytes:
        return self.cipher.decrypt(encrypted_content)
```

## 🚀 Quick Start Commands

### Google Cloud Setup:
```bash
# 1. Create project and enable APIs
gcloud projects create legal-doc-simplifier
gcloud config set project legal-doc-simplifier
gcloud services enable run.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable aiplatform.googleapis.com

# 2. Create storage bucket
gsutil mb gs://legal-docs-bucket

# 3. Deploy backend
gcloud run deploy legal-doc-backend --source backend --allow-unauthenticated

# 4. Deploy frontend
gcloud run deploy legal-doc-frontend --source frontend --allow-unauthenticated
```

### AWS Setup:
```bash
# 1. Create S3 bucket
aws s3 mb s3://legal-docs-bucket

# 2. Create ECR repository
aws ecr create-repository --repository-name legal-doc-backend

# 3. Build and push image
docker build -t legal-doc-backend .
docker tag legal-doc-backend:latest your-account.dkr.ecr.region.amazonaws.com/legal-doc-backend:latest
docker push your-account.dkr.ecr.region.amazonaws.com/legal-doc-backend:latest

# 4. Deploy with ECS
aws ecs create-service --cluster your-cluster --service-name legal-doc-backend --task-definition legal-doc-simplifier
```

## 💰 Cost Optimization

### 1. **Serverless Benefits**
- Pay only for actual usage
- Automatic scaling
- No server management

### 2. **Storage Optimization**
- Use appropriate storage classes
- Implement lifecycle policies
- Compress documents before storage

### 3. **Caching Strategy**
- Cache OCR results
- Use CDN for static assets
- Implement Redis for session data

This cloud integration will make your Legal Document Simplifier production-ready, scalable, and cost-effective!
