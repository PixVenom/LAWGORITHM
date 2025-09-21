from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from typing import Dict, Any
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legal Document Simplifier API",
    description="AI-powered legal document analysis and simplification",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Legal Document Simplifier API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "legal-doc-simplifier"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a legal document
    """
    try:
        logger.info(f"Processing document: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # Simple mock processing for demo
        result = {
            "filename": file.filename,
            "file_size": len(content),
            "status": "processed",
            "text": f"Mock extracted text from {file.filename}. This is a demo version for deployment testing.",
            "language": "en",
            "confidence": 0.95,
            "summaries": {
                "eli5": f"This document ({file.filename}) contains important rules and agreements. It's like a contract that tells you what you can and cannot do.",
                "plain": f"This is a legal document called {file.filename}. It contains terms and conditions that you should understand before agreeing to anything.",
                "detailed": f"Document Analysis: {file.filename}\n\nThis legal document contains various clauses and terms. Key sections include terms of service, liability limitations, and user obligations. Please review all sections carefully before proceeding."
            },
            "risk_assessment": {
                "overall_risk": "medium",
                "high_risk_clauses": ["Liability limitation", "Termination clause"],
                "medium_risk_clauses": ["Payment terms", "Confidentiality"],
                "low_risk_clauses": ["Contact information", "Definitions"]
            },
            "clauses": [
                {
                    "text": "Sample clause 1: Terms of service",
                    "risk_level": "medium",
                    "confidence": 0.8
                },
                {
                    "text": "Sample clause 2: Liability limitation",
                    "risk_level": "high",
                    "confidence": 0.9
                }
            ]
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/chat")
async def chat_with_document(message: str, document_context: str = None):
    """
    Chat with the AI about the document
    """
    try:
        # Simple mock response
        response = {
            "response": f"I can help you understand this legal document. You asked: '{message}'. This is a demo response. In the full version, I would analyze the document content and provide detailed answers.",
            "confidence": 0.8,
            "suggested_questions": [
                "What are the main terms of this agreement?",
                "What are the risks I should be aware of?",
                "Can you explain the liability clause?",
                "What happens if I breach this contract?"
            ]
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.get("/suggested-questions")
async def get_suggested_questions():
    """
    Get suggested questions for the document
    """
    return {
        "questions": [
            "What are the main terms of this agreement?",
            "What are the risks I should be aware of?",
            "Can you explain the liability clause?",
            "What happens if I breach this contract?",
            "What are my rights under this agreement?",
            "What are the payment terms?",
            "How can I terminate this agreement?",
            "What information is considered confidential?"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
