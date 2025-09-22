# 🗄️ Google Cloud Dataset Integration Setup

This guide will help you set up Google Cloud Storage and Firestore to store and manage datasets for your Legal Document Simplifier.

## 🎯 What You'll Get

- **Legal Templates Database** - Store and retrieve legal document templates
- **Risk Patterns Database** - Access risk assessment patterns and keywords
- **Analysis History** - Store and retrieve document analysis results
- **Language Model Configs** - Manage AI model configurations
- **Sample Documents** - Reference legal document examples

## 🚀 Quick Setup (5 minutes)

### Step 1: Set Up Google Cloud

```bash
# Run the fix script
./fix-gcp-setup.sh
```

### Step 2: Enable Firestore

```bash
# Enable Firestore API
gcloud services enable firestore.googleapis.com

# Create Firestore database (choose your region)
gcloud firestore databases create --region=us-central1
```

### Step 3: Upload Sample Datasets

```bash
# Install dependencies
cd backend
pip install -r requirements-cloud.txt

# Upload sample datasets
python ../upload_sample_datasets.py
```

### Step 4: Run Enhanced Backend

```bash
# Use the dataset-enabled backend
python main_with_datasets.py
```

## 📊 Dataset Structure

### Legal Templates Dataset
```json
{
  "contracts": [
    {
      "name": "Service Agreement",
      "template": "This Service Agreement is entered into...",
      "risk_factors": ["liability_limitation", "termination_clause"],
      "common_clauses": ["payment_terms", "confidentiality"],
      "typical_risks": ["high", "medium", "low"]
    }
  ],
  "agreements": [...],
  "disclaimers": [...]
}
```

### Risk Patterns Dataset
```json
{
  "high_risk_keywords": ["liability", "indemnify", "breach"],
  "medium_risk_keywords": ["payment", "confidentiality"],
  "low_risk_keywords": ["contact information", "definitions"],
  "risk_scores": {"high": 0.8, "medium": 0.5, "low": 0.2}
}
```

### Language Models Dataset
```json
{
  "summarization": {
    "eli5": {
      "model": "text-bison@001",
      "prompt_template": "Explain this legal document like I'm 5 years old: {text}",
      "max_tokens": 200
    }
  }
}
```

## 🔧 API Endpoints

### Dataset Management
- `GET /datasets/templates` - Get legal templates
- `GET /datasets/risk-patterns` - Get risk patterns
- `GET /datasets/models` - Get language model configs
- `GET /datasets/list` - List all datasets
- `POST /datasets/upload` - Upload new dataset

### Enhanced Analysis
- `POST /upload` - Upload document with dataset integration
- `GET /analyses/history` - Get analysis history
- `POST /chat` - Chat with enhanced dataset context

## 🎯 Frontend Integration

Your frontend will now receive enhanced data:

```javascript
// Enhanced response from /upload endpoint
{
  "filename": "contract.pdf",
  "summaries": {
    "eli5": "Enhanced explanation using legal templates...",
    "plain": "Analysis using GCP datasets...",
    "detailed": "Comprehensive analysis with template matching..."
  },
  "legal_templates": {
    "matched_templates": [...],
    "suggested_clauses": [...]
  },
  "dataset_info": {
    "templates_loaded": 8,
    "risk_patterns_loaded": 25,
    "data_source": "Google Cloud Storage"
  }
}
```

## 🔄 Data Flow

1. **Document Upload** → Backend processes with GCP datasets
2. **Template Matching** → Compare against legal templates
3. **Risk Assessment** → Use risk patterns for analysis
4. **AI Processing** → Use configured language models
5. **Storage** → Save results to GCP Storage + Firestore
6. **Frontend Display** → Enhanced UI with dataset insights

## 📈 Benefits

### For Users
- **Better Analysis** - More accurate legal document understanding
- **Template Matching** - See how documents compare to standards
- **Risk Insights** - Enhanced risk assessment with patterns
- **History Tracking** - Access previous analyses

### For Developers
- **Scalable Storage** - Google Cloud Storage handles large datasets
- **Real-time Updates** - Firestore for live data synchronization
- **Flexible Queries** - Easy dataset management and retrieval
- **Cost Effective** - Pay only for what you use

## 🛠️ Customization

### Add Your Own Templates
```python
# Upload custom legal templates
custom_templates = {
    "contracts": [
        {
            "name": "Your Custom Contract",
            "template": "Your template content...",
            "risk_factors": ["custom_risk_1", "custom_risk_2"]
        }
    ]
}

await dataset_service.upload_dataset("custom_templates", custom_templates)
```

### Modify Risk Patterns
```python
# Update risk assessment patterns
custom_patterns = {
    "high_risk_keywords": ["your", "custom", "keywords"],
    "risk_scores": {"high": 0.9, "medium": 0.6, "low": 0.3}
}

await dataset_service.upload_dataset("custom_risk_patterns", custom_patterns)
```

## 🚀 Deployment

### Local Development
```bash
cd backend
python main_with_datasets.py
```

### Cloud Run Deployment
```bash
# Update your main.py to use main_with_datasets.py
cp main_with_datasets.py main.py

# Deploy to Cloud Run
./deploy-cloudrun.sh
```

### Railway Deployment
```bash
# Update Railway to use the dataset version
# In railway.json, change startCommand to:
"startCommand": "cd backend && python -m uvicorn main_with_datasets:app --host 0.0.0.0 --port $PORT"
```

## 🎉 Result

Your Legal Document Simplifier now has:
- ✅ **Comprehensive Legal Database** - Templates, patterns, examples
- ✅ **Enhanced AI Analysis** - Better prompts and configurations
- ✅ **Scalable Storage** - Google Cloud Storage + Firestore
- ✅ **Rich Frontend Data** - More detailed and accurate responses
- ✅ **Analysis History** - Track and retrieve previous analyses
- ✅ **Template Matching** - Compare documents to legal standards

**Your app is now a powerful, data-driven legal document analysis platform!** 🚀
