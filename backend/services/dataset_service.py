from google.cloud import storage
from google.cloud import firestore
import json
import os
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatasetService:
    def __init__(self):
        self.storage_client = storage.Client()
        self.db = firestore.Client()
        self.bucket_name = os.getenv('GCP_BUCKET_NAME', 'legal-doc-simplifier-datasets')
        self.bucket = self.storage_client.bucket(self.bucket_name)
        
    async def upload_dataset(self, dataset_name: str, data: Dict[str, Any], user_id: str = "default") -> str:
        """Upload a dataset to Google Cloud Storage"""
        try:
            # Create dataset metadata
            dataset_metadata = {
                "name": dataset_name,
                "user_id": user_id,
                "upload_date": datetime.now().isoformat(),
                "size": len(json.dumps(data)),
                "type": "legal_document_dataset"
            }
            
            # Upload to Cloud Storage
            blob_name = f"datasets/{user_id}/{dataset_name}.json"
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(json.dumps(data, indent=2))
            
            # Store metadata in Firestore
            doc_ref = self.db.collection('datasets').document(f"{user_id}_{dataset_name}")
            doc_ref.set(dataset_metadata)
            
            logger.info(f"Dataset {dataset_name} uploaded successfully")
            return f"gs://{self.bucket_name}/{blob_name}"
            
        except Exception as e:
            logger.error(f"Error uploading dataset: {e}")
            raise
    
    async def get_dataset(self, dataset_name: str, user_id: str = "default") -> Dict[str, Any]:
        """Fetch a dataset from Google Cloud Storage"""
        try:
            blob_name = f"datasets/{user_id}/{dataset_name}.json"
            blob = self.bucket.blob(blob_name)
            
            if not blob.exists():
                raise FileNotFoundError(f"Dataset {dataset_name} not found")
            
            data = json.loads(blob.download_as_text())
            return data
            
        except Exception as e:
            logger.error(f"Error fetching dataset: {e}")
            raise
    
    async def list_datasets(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """List all datasets for a user"""
        try:
            # Query Firestore for user's datasets
            docs = self.db.collection('datasets').where('user_id', '==', user_id).stream()
            
            datasets = []
            for doc in docs:
                dataset_info = doc.to_dict()
                dataset_info['id'] = doc.id
                datasets.append(dataset_info)
            
            return datasets
            
        except Exception as e:
            logger.error(f"Error listing datasets: {e}")
            raise
    
    async def get_legal_templates(self) -> List[Dict[str, Any]]:
        """Get legal document templates from dataset"""
        try:
            # Try to get from user datasets first, fallback to default
            try:
                templates = await self.get_dataset("legal_templates", "default")
            except FileNotFoundError:
                # Return default templates if not found
                templates = {
                    "contracts": [
                        {
                            "name": "Service Agreement",
                            "template": "This Service Agreement is entered into between...",
                            "risk_factors": ["liability_limitation", "termination_clause"],
                            "common_clauses": ["payment_terms", "confidentiality", "intellectual_property"]
                        },
                        {
                            "name": "Employment Contract",
                            "template": "This Employment Agreement is made between...",
                            "risk_factors": ["non_compete", "severance_pay"],
                            "common_clauses": ["job_description", "compensation", "benefits"]
                        }
                    ],
                    "agreements": [
                        {
                            "name": "Non-Disclosure Agreement",
                            "template": "This Non-Disclosure Agreement is entered into...",
                            "risk_factors": ["confidentiality_scope", "duration"],
                            "common_clauses": ["definition", "obligations", "exceptions"]
                        }
                    ]
                }
            
            return templates
            
        except Exception as e:
            logger.error(f"Error getting legal templates: {e}")
            return {}
    
    async def get_risk_patterns(self) -> Dict[str, Any]:
        """Get risk assessment patterns from dataset"""
        try:
            try:
                patterns = await self.get_dataset("risk_patterns", "default")
            except FileNotFoundError:
                # Default risk patterns
                patterns = {
                    "high_risk_keywords": [
                        "liability", "indemnify", "hold harmless", "breach",
                        "termination", "penalty", "damages", "waiver"
                    ],
                    "medium_risk_keywords": [
                        "payment", "confidentiality", "intellectual property",
                        "governing law", "dispute resolution"
                    ],
                    "low_risk_keywords": [
                        "contact information", "definitions", "effective date",
                        "parties", "recitals"
                    ],
                    "risk_scores": {
                        "high": 0.8,
                        "medium": 0.5,
                        "low": 0.2
                    }
                }
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error getting risk patterns: {e}")
            return {}
    
    async def get_language_models(self) -> Dict[str, Any]:
        """Get language model configurations from dataset"""
        try:
            try:
                models = await self.get_dataset("language_models", "default")
            except FileNotFoundError:
                # Default model configurations
                models = {
                    "summarization": {
                        "eli5": {
                            "model": "text-bison@001",
                            "prompt_template": "Explain this legal document like I'm 5 years old: {text}",
                            "max_tokens": 200
                        },
                        "plain": {
                            "model": "text-bison@001", 
                            "prompt_template": "Summarize this legal document in plain language: {text}",
                            "max_tokens": 300
                        },
                        "detailed": {
                            "model": "text-bison@001",
                            "prompt_template": "Provide a detailed analysis of this legal document: {text}",
                            "max_tokens": 500
                        }
                    },
                    "chatbot": {
                        "model": "text-bison@001",
                        "system_prompt": "You are a legal document assistant. Help users understand legal documents.",
                        "max_tokens": 400
                    }
                }
            
            return models
            
        except Exception as e:
            logger.error(f"Error getting language models: {e}")
            return {}
    
    async def store_analysis_result(self, document_id: str, analysis: Dict[str, Any], user_id: str = "default") -> str:
        """Store document analysis results"""
        try:
            # Add metadata
            analysis['document_id'] = document_id
            analysis['user_id'] = user_id
            analysis['analysis_date'] = datetime.now().isoformat()
            
            # Store in Cloud Storage
            blob_name = f"analyses/{user_id}/{document_id}.json"
            blob = self.bucket.blob(blob_name)
            blob.upload_from_string(json.dumps(analysis, indent=2))
            
            # Store reference in Firestore
            doc_ref = self.db.collection('analyses').document(f"{user_id}_{document_id}")
            doc_ref.set({
                "document_id": document_id,
                "user_id": user_id,
                "analysis_date": analysis['analysis_date'],
                "storage_path": f"gs://{self.bucket_name}/{blob_name}",
                "summary": analysis.get('summaries', {}).get('plain', '')[:100] + "..."
            })
            
            return f"gs://{self.bucket_name}/{blob_name}"
            
        except Exception as e:
            logger.error(f"Error storing analysis result: {e}")
            raise
    
    async def get_analysis_history(self, user_id: str = "default", limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's analysis history"""
        try:
            docs = self.db.collection('analyses').where('user_id', '==', user_id).order_by('analysis_date', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            analyses = []
            for doc in docs:
                analysis_info = doc.to_dict()
                analysis_info['id'] = doc.id
                analyses.append(analysis_info)
            
            return analyses
            
        except Exception as e:
            logger.error(f"Error getting analysis history: {e}")
            return []
