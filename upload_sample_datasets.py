#!/usr/bin/env python3
"""
Script to upload sample datasets to Google Cloud Storage
Run this after setting up your GCP credentials
"""

import asyncio
import json
import os
from backend.services.dataset_service import DatasetService

# Sample legal templates dataset
LEGAL_TEMPLATES = {
    "contracts": [
        {
            "name": "Service Agreement",
            "template": "This Service Agreement is entered into between [Company Name] and [Client Name] on [Date]. The terms and conditions are as follows...",
            "risk_factors": ["liability_limitation", "termination_clause", "payment_terms"],
            "common_clauses": ["scope_of_services", "payment_terms", "confidentiality", "intellectual_property", "termination"],
            "typical_risks": ["high", "medium", "low"],
            "jurisdiction": "US"
        },
        {
            "name": "Employment Contract",
            "template": "This Employment Agreement is made between [Employer] and [Employee] on [Date]. The employment terms include...",
            "risk_factors": ["non_compete", "severance_pay", "confidentiality"],
            "common_clauses": ["job_description", "compensation", "benefits", "termination", "confidentiality"],
            "typical_risks": ["medium", "high", "medium"],
            "jurisdiction": "US"
        },
        {
            "name": "Software License Agreement",
            "template": "This Software License Agreement is between [Licensor] and [Licensee] for the use of [Software Name]...",
            "risk_factors": ["intellectual_property", "liability_limitation", "warranty_disclaimer"],
            "common_clauses": ["license_grant", "restrictions", "intellectual_property", "warranty", "limitation_of_liability"],
            "typical_risks": ["high", "high", "medium"],
            "jurisdiction": "US"
        }
    ],
    "agreements": [
        {
            "name": "Non-Disclosure Agreement (NDA)",
            "template": "This Non-Disclosure Agreement is entered into between [Party A] and [Party B] to protect confidential information...",
            "risk_factors": ["confidentiality_scope", "duration", "penalties"],
            "common_clauses": ["definition", "obligations", "exceptions", "duration", "remedies"],
            "typical_risks": ["medium", "medium", "high"],
            "jurisdiction": "US"
        },
        {
            "name": "Partnership Agreement",
            "template": "This Partnership Agreement establishes the terms between [Partner 1] and [Partner 2] for their business partnership...",
            "risk_factors": ["profit_sharing", "decision_making", "dissolution"],
            "common_clauses": ["partnership_terms", "capital_contributions", "profit_loss_sharing", "management", "dissolution"],
            "typical_risks": ["high", "high", "high"],
            "jurisdiction": "US"
        }
    ],
    "disclaimers": [
        {
            "name": "Website Terms of Service",
            "template": "These Terms of Service govern your use of [Website Name]. By using our service, you agree to these terms...",
            "risk_factors": ["liability_limitation", "user_conduct", "content_policy"],
            "common_clauses": ["acceptance", "user_obligations", "prohibited_uses", "intellectual_property", "disclaimers"],
            "typical_risks": ["medium", "medium", "low"],
            "jurisdiction": "US"
        }
    ]
}

# Risk assessment patterns
RISK_PATTERNS = {
    "high_risk_keywords": [
        "liability", "indemnify", "hold harmless", "breach", "penalty",
        "termination", "damages", "waiver", "disclaimer", "exclusion",
        "limitation", "consequential", "punitive", "liquidated", "forfeit"
    ],
    "medium_risk_keywords": [
        "payment", "confidentiality", "intellectual property", "governing law",
        "dispute resolution", "arbitration", "jurisdiction", "severability",
        "assignment", "modification", "entire agreement", "force majeure"
    ],
    "low_risk_keywords": [
        "contact information", "definitions", "effective date", "parties",
        "recitals", "whereas", "now therefore", "witness", "signature",
        "notices", "headings", "counterparts"
    ],
    "risk_scores": {
        "high": 0.8,
        "medium": 0.5,
        "low": 0.2
    },
    "clause_patterns": {
        "liability_limitation": {
            "keywords": ["liability", "damages", "limitation", "exclusion"],
            "risk_level": "high",
            "common_phrases": ["to the maximum extent permitted by law", "in no event shall"]
        },
        "termination_clause": {
            "keywords": ["termination", "breach", "default", "cure"],
            "risk_level": "high",
            "common_phrases": ["immediate termination", "material breach", "cure period"]
        },
        "confidentiality": {
            "keywords": ["confidential", "proprietary", "non-disclosure"],
            "risk_level": "medium",
            "common_phrases": ["confidential information", "proprietary data"]
        }
    }
}

# Language model configurations
LANGUAGE_MODELS = {
    "summarization": {
        "eli5": {
            "model": "text-bison@001",
            "prompt_template": "Explain this legal document like I'm 5 years old. Focus on what the person can and cannot do: {text}",
            "max_tokens": 200,
            "temperature": 0.3
        },
        "plain": {
            "model": "text-bison@001",
            "prompt_template": "Summarize this legal document in plain, easy-to-understand language. Highlight key points and obligations: {text}",
            "max_tokens": 300,
            "temperature": 0.4
        },
        "detailed": {
            "model": "text-bison@001",
            "prompt_template": "Provide a detailed legal analysis of this document. Include clause-by-clause breakdown, risk assessment, and recommendations: {text}",
            "max_tokens": 500,
            "temperature": 0.5
        }
    },
    "chatbot": {
        "model": "text-bison@001",
        "system_prompt": "You are a legal document assistant with access to comprehensive legal templates and risk patterns. Help users understand legal documents by referencing similar templates and identifying potential risks.",
        "max_tokens": 400,
        "temperature": 0.6
    },
    "risk_assessment": {
        "model": "text-bison@001",
        "prompt_template": "Analyze this legal document for potential risks. Consider liability clauses, termination terms, payment obligations, and confidentiality requirements: {text}",
        "max_tokens": 300,
        "temperature": 0.3
    }
}

# Sample legal document examples
SAMPLE_DOCUMENTS = {
    "service_agreement_sample": {
        "title": "Sample Service Agreement",
        "content": "This Service Agreement is entered into between ABC Company and XYZ Client on January 1, 2024. ABC Company agrees to provide software development services. The client agrees to pay $10,000 per month. Either party may terminate this agreement with 30 days notice. ABC Company's liability is limited to the amount paid by the client in the last 12 months.",
        "document_type": "service_agreement",
        "risk_level": "medium",
        "key_clauses": ["service_description", "payment_terms", "termination", "liability_limitation"]
    },
    "nda_sample": {
        "title": "Sample Non-Disclosure Agreement",
        "content": "This Non-Disclosure Agreement is between TechCorp and StartupXYZ. Both parties agree to keep confidential information secret for 3 years. Confidential information includes business plans, technical specifications, and customer lists. This agreement survives termination of any other agreements between the parties.",
        "document_type": "nda",
        "risk_level": "medium",
        "key_clauses": ["confidentiality_definition", "duration", "survival_clause"]
    }
}

async def upload_sample_datasets():
    """Upload all sample datasets to Google Cloud Storage"""
    print("🚀 Uploading sample datasets to Google Cloud Storage...")
    
    try:
        dataset_service = DatasetService()
        
        # Upload legal templates
        print("📋 Uploading legal templates...")
        await dataset_service.upload_dataset("legal_templates", LEGAL_TEMPLATES, "default")
        print("✅ Legal templates uploaded")
        
        # Upload risk patterns
        print("⚠️ Uploading risk patterns...")
        await dataset_service.upload_dataset("risk_patterns", RISK_PATTERNS, "default")
        print("✅ Risk patterns uploaded")
        
        # Upload language models
        print("🤖 Uploading language model configurations...")
        await dataset_service.upload_dataset("language_models", LANGUAGE_MODELS, "default")
        print("✅ Language models uploaded")
        
        # Upload sample documents
        print("📄 Uploading sample documents...")
        await dataset_service.upload_dataset("sample_documents", SAMPLE_DOCUMENTS, "default")
        print("✅ Sample documents uploaded")
        
        print("\n🎉 All datasets uploaded successfully!")
        print("\n📊 Dataset Summary:")
        print(f"   - Legal Templates: {len(LEGAL_TEMPLATES['contracts']) + len(LEGAL_TEMPLATES['agreements']) + len(LEGAL_TEMPLATES['disclaimers'])} templates")
        print(f"   - Risk Patterns: {len(RISK_PATTERNS['high_risk_keywords']) + len(RISK_PATTERNS['medium_risk_keywords']) + len(RISK_PATTERNS['low_risk_keywords'])} keywords")
        print(f"   - Language Models: {len(LANGUAGE_MODELS)} model configurations")
        print(f"   - Sample Documents: {len(SAMPLE_DOCUMENTS)} examples")
        
        print("\n🚀 Your backend can now use these datasets for enhanced analysis!")
        
    except Exception as e:
        print(f"❌ Error uploading datasets: {e}")
        print("\n🔧 Make sure you have:")
        print("   1. Set up Google Cloud credentials")
        print("   2. Created a storage bucket")
        print("   3. Enabled Firestore API")
        print("   4. Run: ./fix-gcp-setup.sh")

if __name__ == "__main__":
    asyncio.run(upload_sample_datasets())
