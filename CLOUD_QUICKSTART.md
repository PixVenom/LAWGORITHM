# Cloud Integration Quick Start Guide

Get your Legal Document Simplifier running in the cloud in 15 minutes!

## 🚀 Quick Start Options

### Option 1: Google Cloud Platform (Recommended)

#### Prerequisites:
- Google Cloud account
- gcloud CLI installed
- Docker installed

#### Steps:

1. **Set up Google Cloud Project:**
```bash
# Create project
gcloud projects create your-project-id
gcloud config set project your-project-id

# Enable billing (required for APIs)
# Go to: https://console.cloud.google.com/billing
```

2. **Deploy with one command:**
```bash
./deploy-cloud.sh --provider gcp --project-id your-project-id
```

3. **Set up authentication:**
```bash
# Download service account key
gcloud iam service-accounts create legal-doc-service
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:legal-doc-service@your-project-id.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
gcloud iam service-accounts keys create credentials.json \
    --iam-account=legal-doc-service@your-project-id.iam.gserviceaccount.com
```

4. **Access your app:**
- Frontend: `https://your-service-frontend-xxx-uc.a.run.app`
- Backend: `https://your-service-backend-xxx-uc.a.run.app`

### Option 2: AWS

#### Prerequisites:
- AWS account
- AWS CLI configured
- Docker installed

#### Steps:

1. **Configure AWS CLI:**
```bash
aws configure
# Enter your Access Key ID, Secret Access Key, and region
```

2. **Deploy:**
```bash
./deploy-cloud.sh --provider aws --project-id your-aws-account-id --region us-east-1
```

3. **Set up IAM roles and policies** (see full documentation)

### Option 3: Azure

#### Prerequisites:
- Azure account
- Azure CLI installed
- Docker installed

#### Steps:

1. **Login to Azure:**
```bash
az login
az account set --subscription your-subscription-id
```

2. **Deploy:**
```bash
./deploy-cloud.sh --provider azure --project-id your-subscription-id --region eastus
```

## 🔧 Environment Configuration

### Google Cloud Environment Variables:
```bash
# Set in Cloud Run or .env file
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GCP_BUCKET_NAME=legal-docs-bucket
USE_CLOUD_OCR=true
USE_VERTEX_AI=true
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
```

### AWS Environment Variables:
```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=legal-docs-bucket
AWS_REGION=us-east-1
USE_AWS_SERVICES=true
```

### Azure Environment Variables:
```bash
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_VISION_ENDPOINT=your-vision-endpoint
AZURE_VISION_KEY=your-vision-key
USE_AZURE_SERVICES=true
```

## 📊 What You Get with Cloud Integration

### Enhanced Features:
- ✅ **Cloud OCR** - Google Vision API, AWS Textract, or Azure Computer Vision
- ✅ **Cloud Storage** - Scalable document storage
- ✅ **AI Services** - Vertex AI, OpenAI, or Azure OpenAI
- ✅ **Auto-scaling** - Handles traffic spikes automatically
- ✅ **Global CDN** - Fast content delivery worldwide
- ✅ **Monitoring** - Built-in logging and metrics
- ✅ **Security** - Enterprise-grade security features

### Cost Benefits:
- 💰 **Pay-per-use** - Only pay for what you use
- 💰 **No server management** - Focus on your app, not infrastructure
- 💰 **Automatic scaling** - Scale up/down based on demand
- 💰 **Free tiers** - Most services offer generous free tiers

## 🔐 Security Setup

### 1. Authentication:
```python
# Add to your backend
from services.auth_service import CloudAuthService

auth_service = CloudAuthService()

@app.post("/upload")
async def upload_document(file: UploadFile, token: str = Depends(verify_token)):
    # Your upload logic here
    pass
```

### 2. Data Encryption:
```python
# Add to your services
from services.encryption_service import EncryptionService

encryption = EncryptionService()
encrypted_content = encryption.encrypt_document(file_content)
```

### 3. Access Control:
```python
# Implement user-based access
@app.get("/documents/{document_id}")
async def get_document(document_id: str, user_id: str = Depends(get_current_user)):
    # Verify user owns the document
    pass
```

## 📈 Monitoring Setup

### Google Cloud Monitoring:
```python
# Add to your services
from services.monitoring_service import CloudMonitoringService

monitoring = CloudMonitoringService()

# Log metrics
monitoring.log_document_processed(user_id, processing_time)
```

### AWS CloudWatch:
```python
# Add to your services
from services.aws_monitoring import AWSMonitoringService

monitoring = AWSMonitoringService()

# Log metrics
monitoring.log_metric("DocumentsProcessed", 1)
```

## 🚀 Production Checklist

### Before Going Live:
- [ ] Set up proper authentication
- [ ] Configure SSL certificates
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategies
- [ ] Set up CI/CD pipeline
- [ ] Configure custom domain
- [ ] Set up rate limiting
- [ ] Configure CORS properly
- [ ] Set up error tracking
- [ ] Configure logging levels

### Performance Optimization:
- [ ] Enable CDN for static assets
- [ ] Implement caching strategies
- [ ] Optimize database queries
- [ ] Use connection pooling
- [ ] Implement request compression
- [ ] Set up auto-scaling policies

## 🆘 Troubleshooting

### Common Issues:

1. **Authentication Errors:**
```bash
# Check service account permissions
gcloud projects get-iam-policy your-project-id
```

2. **Storage Access Issues:**
```bash
# Verify bucket permissions
gsutil iam get gs://your-bucket-name
```

3. **API Quotas Exceeded:**
```bash
# Check quotas in Google Cloud Console
# Or increase limits in AWS/Azure
```

4. **Deployment Failures:**
```bash
# Check logs
gcloud run services logs read your-service-name --region=your-region
```

## 📞 Support

### Getting Help:
- 📚 **Documentation**: Check the full CLOUD_INTEGRATION.md
- 🐛 **Issues**: Create GitHub issues for bugs
- 💬 **Community**: Join our Discord/Slack
- 📧 **Email**: support@legal-doc-simplifier.com

### Useful Commands:
```bash
# Check deployment status
gcloud run services list

# View logs
gcloud run services logs read your-service-name

# Update service
gcloud run services update your-service-name --image=gcr.io/your-project/your-image

# Scale service
gcloud run services update your-service-name --concurrency=1000 --max-instances=10
```

## 🎯 Next Steps

After successful cloud deployment:

1. **Custom Domain**: Set up your own domain
2. **SSL Certificate**: Enable HTTPS
3. **Monitoring**: Set up alerts and dashboards
4. **Backup**: Configure automated backups
5. **CI/CD**: Set up automated deployments
6. **Analytics**: Add usage analytics
7. **Multi-region**: Deploy to multiple regions
8. **Load Testing**: Test under high load

---

**🎉 Congratulations! Your Legal Document Simplifier is now running in the cloud with enterprise-grade features!**
