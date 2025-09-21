import re
import logging
from typing import List, Dict, Any
import asyncio

logger = logging.getLogger(__name__)

class SegmentationService:
    def __init__(self):
        # Common legal clause patterns
        self.clause_patterns = [
            r'(?:^|\n)\s*(?:Article|Section|Clause|Paragraph)\s+\d+[\.\)\:]\s*',
            r'(?:^|\n)\s*\d+[\.\)]\s*',
            r'(?:^|\n)\s*[a-z]\)\s*',
            r'(?:^|\n)\s*\([a-z]\)\s*',
            r'(?:^|\n)\s*[ivx]+\)\s*',
            r'(?:^|\n)\s*\([ivx]+\)\s*',
            r'(?:^|\n)\s*WHEREAS\s+',
            r'(?:^|\n)\s*NOW\s+THEREFORE\s+',
            r'(?:^|\n)\s*IN\s+WITNESS\s+WHEREOF\s+',
            r'(?:^|\n)\s*THEREFORE\s+',
            r'(?:^|\n)\s*FURTHERMORE\s+',
            r'(?:^|\n)\s*MOREOVER\s+',
            r'(?:^|\n)\s*HOWEVER\s+',
            r'(?:^|\n)\s*NOTWITHSTANDING\s+',
            r'(?:^|\n)\s*SUBJECT\s+TO\s+',
            r'(?:^|\n)\s*PROVIDED\s+THAT\s+',
            r'(?:^|\n)\s*IN\s+THE\s+EVENT\s+THAT\s+',
            r'(?:^|\n)\s*IN\s+CASE\s+OF\s+',
            r'(?:^|\n)\s*IF\s+',
            r'(?:^|\n)\s*UNLESS\s+',
            r'(?:^|\n)\s*EXCEPT\s+',
            r'(?:^|\n)\s*NOTWITHSTANDING\s+',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in self.clause_patterns]
    
    async def segment_clauses(self, text: str) -> List[Dict[str, Any]]:
        """
        Segment the legal document into clauses
        """
        try:
            if not text.strip():
                return []
            
            # Run segmentation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            clauses = await loop.run_in_executor(None, self._segment_text, text)
            
            return clauses
            
        except Exception as e:
            logger.error(f"Error segmenting clauses: {e}")
            return [{
                "id": 1,
                "text": text,
                "type": "unknown",
                "start_index": 0,
                "end_index": len(text),
                "confidence": 0.1
            }]
    
    def _segment_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Perform the actual text segmentation
        """
        clauses = []
        current_clause = ""
        clause_id = 1
        start_index = 0
        
        # Split text into sentences first
        sentences = self._split_into_sentences(text)
        
        for i, sentence in enumerate(sentences):
            # Check if this sentence starts a new clause
            if self._is_clause_start(sentence):
                # Save previous clause if it exists
                if current_clause.strip():
                    clauses.append({
                        "id": clause_id,
                        "text": current_clause.strip(),
                        "type": self._classify_clause_type(current_clause),
                        "start_index": start_index,
                        "end_index": start_index + len(current_clause),
                        "confidence": self._calculate_confidence(current_clause)
                    })
                    clause_id += 1
                
                # Start new clause
                current_clause = sentence
                start_index = text.find(sentence)
            else:
                # Continue current clause
                current_clause += " " + sentence
        
        # Add the last clause
        if current_clause.strip():
            clauses.append({
                "id": clause_id,
                "text": current_clause.strip(),
                "type": self._classify_clause_type(current_clause),
                "start_index": start_index,
                "end_index": start_index + len(current_clause),
                "confidence": self._calculate_confidence(current_clause)
            })
        
        # If no clauses were found, treat the entire text as one clause
        if not clauses:
            clauses.append({
                "id": 1,
                "text": text,
                "type": "general",
                "start_index": 0,
                "end_index": len(text),
                "confidence": 0.5
            })
        
        return clauses
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        """
        # Simple sentence splitting - can be improved with NLTK or spaCy
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _is_clause_start(self, sentence: str) -> bool:
        """
        Check if a sentence starts a new clause
        """
        for pattern in self.compiled_patterns:
            if pattern.match(sentence):
                return True
        return False
    
    def _classify_clause_type(self, clause_text: str) -> str:
        """
        Classify the type of clause
        """
        clause_lower = clause_text.lower()
        
        # Define clause type patterns
        type_patterns = {
            "definition": [
                r'\b(?:means?|shall mean|refers to|is defined as)\b',
                r'\b(?:for the purposes? of|in this agreement)\b'
            ],
            "obligation": [
                r'\b(?:shall|must|will|agree to|undertake to)\b',
                r'\b(?:responsible for|liable for|bound to)\b'
            ],
            "prohibition": [
                r'\b(?:shall not|must not|will not|cannot|may not)\b',
                r'\b(?:prohibited|forbidden|restricted)\b'
            ],
            "condition": [
                r'\b(?:if|unless|provided that|subject to)\b',
                r'\b(?:in the event that|in case of)\b'
            ],
            "termination": [
                r'\b(?:terminate|end|expire|cease)\b',
                r'\b(?:breach|default|violation)\b'
            ],
            "liability": [
                r'\b(?:liability|damages|indemnify|hold harmless)\b',
                r'\b(?:responsible|accountable|liable)\b'
            ],
            "payment": [
                r'\b(?:payment|fee|cost|expense|charge)\b',
                r'\b(?:due|payable|remit|transfer)\b'
            ],
            "confidentiality": [
                r'\b(?:confidential|proprietary|secret|private)\b',
                r'\b(?:disclose|reveal|share|divulge)\b'
            ]
        }
        
        # Check for clause types
        for clause_type, patterns in type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, clause_lower):
                    return clause_type
        
        return "general"
    
    def _calculate_confidence(self, clause_text: str) -> float:
        """
        Calculate confidence score for clause segmentation
        """
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on legal keywords
        legal_keywords = [
            'shall', 'must', 'will', 'agree', 'party', 'contract', 'agreement',
            'liability', 'damages', 'breach', 'terminate', 'confidential',
            'payment', 'fee', 'obligation', 'right', 'duty', 'responsibility'
        ]
        
        clause_lower = clause_text.lower()
        keyword_count = sum(1 for keyword in legal_keywords if keyword in clause_lower)
        confidence += min(0.3, keyword_count * 0.05)
        
        # Increase confidence for longer clauses (more likely to be complete)
        if len(clause_text) > 100:
            confidence += 0.1
        elif len(clause_text) > 50:
            confidence += 0.05
        
        # Increase confidence for clauses with proper punctuation
        if clause_text.endswith(('.', '!', '?')):
            confidence += 0.1
        
        return min(1.0, confidence)
