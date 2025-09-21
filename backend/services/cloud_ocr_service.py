import os
import logging
from typing import Dict, Any
import asyncio
import uuid
from datetime import datetime

try:
    from google.cloud import vision
    from google.cloud import storage
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False

logger = logging.getLogger(__name__)

class CloudOCRService:
    def __init__(self):
        self.use_cloud = os.getenv("USE_CLOUD_OCR", "False").lower() == "true"
        self.bucket_name = os.getenv("GCP_BUCKET_NAME", "legal-docs-bucket")
        
        if self.use_cloud and GOOGLE_CLOUD_AVAILABLE:
            try:
                self.vision_client = vision.ImageAnnotatorClient()
                self.storage_client = storage.Client()
                logger.info("Google Cloud Vision and Storage initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Cloud services: {e}")
                self.use_cloud = False
        else:
            self.use_cloud = False
    
    async def process_document_cloud(self, file_path: str, user_id: str = None) -> Dict[str, Any]:
        """
        Process document using Google Cloud Vision API with cloud storage
        """
        if not self.use_cloud:
            raise Exception("Cloud OCR not enabled or not available")
        
        try:
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            file_extension = file_path.split('.')[-1]
            blob_name = f"documents/{user_id or 'anonymous'}/{file_id}.{file_extension}"
            
            # Upload to Cloud Storage
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            
            with open(file_path, 'rb') as file:
                blob.upload_from_file(file)
            
            logger.info(f"File uploaded to cloud storage: {blob_name}")
            
            # Process with Vision API
            image = vision.Image()
            image.source.image_uri = f"gs://{self.bucket_name}/{blob_name}"
            
            # Use document text detection for better results
            response = self.vision_client.document_text_detection(image=image)
            
            if response.error.message:
                raise Exception(f"Google Vision API error: {response.error.message}")
            
            # Extract text and confidence
            full_text = response.full_text_annotation.text if response.full_text_annotation else ""
            confidence = 0.95  # Google Vision doesn't provide confidence for document detection
            
            # Get document structure if available
            document_structure = self._extract_document_structure(response)
            
            return {
                "text": full_text,
                "confidence": confidence,
                "method": "Google Cloud Vision API",
                "cloud_url": f"gs://{self.bucket_name}/{blob_name}",
                "public_url": blob.public_url,
                "file_id": file_id,
                "document_structure": document_structure,
                "processed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Cloud OCR processing failed: {e}")
            raise
    
    def _extract_document_structure(self, response) -> Dict[str, Any]:
        """
        Extract document structure from Vision API response
        """
        structure = {
            "pages": [],
            "blocks": [],
            "paragraphs": [],
            "words": []
        }
        
        if not response.full_text_annotation:
            return structure
        
        for page in response.full_text_annotation.pages:
            page_info = {
                "page_number": len(structure["pages"]) + 1,
                "width": page.width,
                "height": page.height,
                "confidence": page.confidence if hasattr(page, 'confidence') else 0.95
            }
            structure["pages"].append(page_info)
            
            for block in page.blocks:
                block_info = {
                    "block_type": block.block_type.name,
                    "confidence": block.confidence if hasattr(block, 'confidence') else 0.95,
                    "bounding_box": self._get_bounding_box(block.bounding_box)
                }
                structure["blocks"].append(block_info)
                
                for paragraph in block.paragraphs:
                    paragraph_text = ""
                    for word in paragraph.words:
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        paragraph_text += word_text + " "
                        
                        word_info = {
                            "text": word_text,
                            "confidence": word.confidence if hasattr(word, 'confidence') else 0.95,
                            "bounding_box": self._get_bounding_box(word.bounding_box)
                        }
                        structure["words"].append(word_info)
                    
                    paragraph_info = {
                        "text": paragraph_text.strip(),
                        "confidence": paragraph.confidence if hasattr(paragraph, 'confidence') else 0.95,
                        "bounding_box": self._get_bounding_box(paragraph.bounding_box)
                    }
                    structure["paragraphs"].append(paragraph_info)
        
        return structure
    
    def _get_bounding_box(self, bounding_box) -> Dict[str, Any]:
        """
        Convert bounding box to dictionary format
        """
        if not bounding_box or not bounding_box.vertices:
            return {"x": 0, "y": 0, "width": 0, "height": 0}
        
        vertices = bounding_box.vertices
        x_coords = [v.x for v in vertices]
        y_coords = [v.y for v in vertices]
        
        return {
            "x": min(x_coords),
            "y": min(y_coords),
            "width": max(x_coords) - min(x_coords),
            "height": max(y_coords) - min(y_coords)
        }
    
    async def get_document_from_cloud(self, file_id: str, user_id: str = None) -> bytes:
        """
        Retrieve document from cloud storage
        """
        if not self.use_cloud:
            raise Exception("Cloud storage not enabled")
        
        try:
            blob_name = f"documents/{user_id or 'anonymous'}/{file_id}"
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            
            return blob.download_as_bytes()
            
        except Exception as e:
            logger.error(f"Failed to retrieve document from cloud: {e}")
            raise
    
    async def delete_document_from_cloud(self, file_id: str, user_id: str = None) -> bool:
        """
        Delete document from cloud storage
        """
        if not self.use_cloud:
            return False
        
        try:
            blob_name = f"documents/{user_id or 'anonymous'}/{file_id}"
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            
            blob.delete()
            logger.info(f"Document deleted from cloud storage: {blob_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete document from cloud: {e}")
            return False
    
    def generate_signed_url(self, file_id: str, user_id: str = None, expiration_minutes: int = 60) -> str:
        """
        Generate a signed URL for document access
        """
        if not self.use_cloud:
            return None
        
        try:
            from datetime import timedelta
            
            blob_name = f"documents/{user_id or 'anonymous'}/{file_id}"
            bucket = self.storage_client.bucket(self.bucket_name)
            blob = bucket.blob(blob_name)
            
            return blob.generate_signed_url(
                expiration=datetime.utcnow() + timedelta(minutes=expiration_minutes),
                method='GET'
            )
            
        except Exception as e:
            logger.error(f"Failed to generate signed URL: {e}")
            return None
