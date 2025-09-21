from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import tempfile
import logging
from dotenv import load_dotenv

from services.ocr_service import OCRService
from services.language_service import LanguageService
from services.segmentation_service import SegmentationService
from services.summarization_service import SummarizationService
from services.risk_service import RiskService
from services.chatbot_service import ChatbotService
from services.pdf_service import PDFService

# Load environment variables
load_dotenv()

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
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ocr_service = OCRService()
language_service = LanguageService()
segmentation_service = SegmentationService()
summarization_service = SummarizationService()
risk_service = RiskService()
chatbot_service = ChatbotService()
pdf_service = PDFService()

# Pydantic models
class DocumentAnalysis(BaseModel):
    text: str
    language: str
    confidence: float
    clauses: List[Dict[str, Any]]
    summaries: Dict[str, str]
    risk_scores: List[Dict[str, Any]]

class ChatMessage(BaseModel):
    message: str
    document_context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    confidence: float

@app.get("/")
async def root():
    return {"message": "Legal Document Simplifier API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/upload", response_model=DocumentAnalysis)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and analyze a legal document (PDF or image)
    """
    try:
        # Validate file type
        if not file.content_type.startswith(('image/', 'application/pdf')):
            raise HTTPException(status_code=400, detail="File must be an image or PDF")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Perform OCR
            logger.info(f"Performing OCR on {file.filename}")
            ocr_result = await ocr_service.extract_text(tmp_file_path)
            
            # Detect language
            logger.info("Detecting language")
            language_result = await language_service.detect_language(ocr_result['text'])
            
            # Segment clauses
            logger.info("Segmenting clauses")
            clauses = await segmentation_service.segment_clauses(ocr_result['text'])
            
            # Generate summaries
            logger.info("Generating summaries")
            summaries = await summarization_service.generate_summaries(ocr_result['text'])
            
            # Calculate risk scores
            logger.info("Calculating risk scores")
            risk_scores = await risk_service.calculate_risk_scores(clauses)
            
            return DocumentAnalysis(
                text=ocr_result['text'],
                language=language_result['language'],
                confidence=language_result['confidence'],
                clauses=clauses,
                summaries=summaries,
                risk_scores=risk_scores
            )
            
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_document(chat_message: ChatMessage):
    """
    Chat with the AI about the document
    """
    try:
        response = await chatbot_service.get_response(
            message=chat_message.message,
            document_context=chat_message.document_context
        )
        return ChatResponse(
            response=response['response'],
            confidence=response['confidence']
        )
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@app.post("/export-pdf")
async def export_pdf(document_data: DocumentAnalysis):
    """
    Export document analysis as PDF
    """
    try:
        pdf_path = await pdf_service.create_pdf(document_data)
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename='legal_document_analysis.pdf'
        )
    except Exception as e:
        logger.error(f"Error creating PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating PDF: {str(e)}")

@app.get("/models/status")
async def get_models_status():
    """
    Get status of AI models
    """
    return {
        "ocr": "ready",
        "language_detection": "ready",
        "summarization": "ready",
        "risk_assessment": "ready",
        "chatbot": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )
