import os
import logging
from typing import Dict, Any
import asyncio
from PIL import Image
import PyPDF2
import io

try:
    from google.cloud import vision
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        self.use_google_vision = os.getenv("USE_GOOGLE_VISION", "True").lower() == "true"
        self.tesseract_path = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
        
        if self.use_google_vision and GOOGLE_VISION_AVAILABLE:
            try:
                self.vision_client = vision.ImageAnnotatorClient()
                logger.info("Google Vision API initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Vision: {e}")
                self.use_google_vision = False
        
        if TESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
            logger.info("Tesseract OCR initialized")
    
    async def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF or image file
        """
        try:
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                return await self._extract_from_pdf(file_path)
            else:
                return await self._extract_from_image(file_path)
                
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            raise
    
    async def _extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from PDF file
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return {
                    "text": text.strip(),
                    "confidence": 0.9,
                    "method": "PyPDF2"
                }
        except Exception as e:
            logger.error(f"Error extracting from PDF: {e}")
            raise
    
    async def _extract_from_image(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from image file using Google Vision or Tesseract
        """
        try:
            if self.use_google_vision and GOOGLE_VISION_AVAILABLE:
                return await self._extract_with_google_vision(file_path)
            elif TESSERACT_AVAILABLE:
                return await self._extract_with_tesseract(file_path)
            else:
                raise Exception("No OCR service available")
                
        except Exception as e:
            logger.error(f"Error extracting from image: {e}")
            raise
    
    async def _extract_with_google_vision(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text using Google Vision API
        """
        try:
            with open(file_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            response = self.vision_client.text_detection(image=image)
            
            if response.error.message:
                raise Exception(f"Google Vision API error: {response.error.message}")
            
            texts = response.text_annotations
            if texts:
                full_text = texts[0].description
                confidence = 0.95  # Google Vision doesn't provide confidence for text detection
                
                return {
                    "text": full_text,
                    "confidence": confidence,
                    "method": "Google Vision API"
                }
            else:
                return {
                    "text": "",
                    "confidence": 0.0,
                    "method": "Google Vision API"
                }
                
        except Exception as e:
            logger.warning(f"Google Vision failed: {e}")
            if TESSERACT_AVAILABLE:
                return await self._extract_with_tesseract(file_path)
            else:
                raise
    
    async def _extract_with_tesseract(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text using Tesseract OCR
        """
        try:
            # Run OCR in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(
                None, 
                lambda: pytesseract.image_to_string(Image.open(file_path))
            )
            
            return {
                "text": text.strip(),
                "confidence": 0.8,  # Tesseract confidence estimation
                "method": "Tesseract OCR"
            }
            
        except Exception as e:
            logger.error(f"Tesseract OCR failed: {e}")
            raise
