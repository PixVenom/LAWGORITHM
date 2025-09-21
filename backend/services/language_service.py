import os
import logging
from typing import Dict, Any, List
import asyncio

try:
    from google.cloud import translate_v2 as translate
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    import langdetect
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

logger = logging.getLogger(__name__)

class LanguageService:
    def __init__(self):
        self.use_google_translate = os.getenv("USE_GOOGLE_TRANSLATE", "True").lower() == "true"
        
        if self.use_google_translate and GOOGLE_TRANSLATE_AVAILABLE:
            try:
                self.translate_client = translate.Client()
                logger.info("Google Translate API initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Translate: {e}")
                self.use_google_translate = False
        
        if LANGDETECT_AVAILABLE:
            logger.info("LangDetect library initialized")
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the input text
        """
        try:
            if not text.strip():
                return {
                    "language": "unknown",
                    "confidence": 0.0,
                    "method": "none"
                }
            
            if self.use_google_translate and GOOGLE_TRANSLATE_AVAILABLE:
                return await self._detect_with_google_translate(text)
            elif LANGDETECT_AVAILABLE:
                return await self._detect_with_langdetect(text)
            else:
                # Fallback to simple heuristics
                return await self._detect_with_heuristics(text)
                
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return await self._detect_with_heuristics(text)
    
    async def _detect_with_google_translate(self, text: str) -> Dict[str, Any]:
        """
        Detect language using Google Translate API
        """
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.translate_client.detect_language(text)
            )
            
            return {
                "language": result['language'],
                "confidence": result['confidence'],
                "method": "Google Translate API"
            }
            
        except Exception as e:
            logger.warning(f"Google Translate detection failed: {e}")
            if LANGDETECT_AVAILABLE:
                return await self._detect_with_langdetect(text)
            else:
                return await self._detect_with_heuristics(text)
    
    async def _detect_with_langdetect(self, text: str) -> Dict[str, Any]:
        """
        Detect language using langdetect library
        """
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: langdetect.detect(text)
            )
            
            return {
                "language": result,
                "confidence": 0.8,  # langdetect doesn't provide confidence
                "method": "LangDetect"
            }
            
        except Exception as e:
            logger.warning(f"LangDetect failed: {e}")
            return await self._detect_with_heuristics(text)
    
    async def _detect_with_heuristics(self, text: str) -> Dict[str, Any]:
        """
        Simple heuristic-based language detection
        """
        try:
            # Simple heuristics for common languages
            text_lower = text.lower()
            
            # English indicators
            english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
            english_count = sum(1 for word in english_words if word in text_lower)
            
            # Spanish indicators
            spanish_words = ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le']
            spanish_count = sum(1 for word in spanish_words if word in text_lower)
            
            # French indicators
            french_words = ['le', 'la', 'de', 'et', 'à', 'un', 'il', 'que', 'ne', 'se', 'ce', 'pas', 'son', 'avec']
            french_count = sum(1 for word in french_words if word in text_lower)
            
            # German indicators
            german_words = ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für', 'ist']
            german_count = sum(1 for word in german_words if word in text_lower)
            
            # Determine language based on word counts
            if english_count > max(spanish_count, french_count, german_count):
                return {
                    "language": "en",
                    "confidence": min(0.7, english_count / 10),
                    "method": "Heuristics"
                }
            elif spanish_count > max(english_count, french_count, german_count):
                return {
                    "language": "es",
                    "confidence": min(0.7, spanish_count / 10),
                    "method": "Heuristics"
                }
            elif french_count > max(english_count, spanish_count, german_count):
                return {
                    "language": "fr",
                    "confidence": min(0.7, french_count / 10),
                    "method": "Heuristics"
                }
            elif german_count > max(english_count, spanish_count, french_count):
                return {
                    "language": "de",
                    "confidence": min(0.7, german_count / 10),
                    "method": "Heuristics"
                }
            else:
                return {
                    "language": "en",  # Default to English
                    "confidence": 0.3,
                    "method": "Heuristics"
                }
                
        except Exception as e:
            logger.error(f"Heuristic detection failed: {e}")
            return {
                "language": "en",
                "confidence": 0.1,
                "method": "Fallback"
            }
    
    async def translate_text(self, text: str, target_language: str = "en") -> Dict[str, Any]:
        """
        Translate text to target language
        """
        try:
            if self.use_google_translate and GOOGLE_TRANSLATE_AVAILABLE:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: self.translate_client.translate(text, target_language=target_language)
                )
                
                return {
                    "translated_text": result['translatedText'],
                    "source_language": result['detectedSourceLanguage'],
                    "target_language": target_language,
                    "method": "Google Translate API"
                }
            else:
                return {
                    "translated_text": text,  # Return original if no translation available
                    "source_language": "unknown",
                    "target_language": target_language,
                    "method": "No translation available"
                }
                
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return {
                "translated_text": text,
                "source_language": "unknown",
                "target_language": target_language,
                "method": "Translation failed"
            }
