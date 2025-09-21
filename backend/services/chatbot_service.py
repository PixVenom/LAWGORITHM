import os
import logging
from typing import Dict, Any, List
import asyncio

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from google.cloud import aiplatform
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self):
        self.use_openai = os.getenv("USE_OPENAI", "True").lower() == "true"
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_vertex_ai = os.getenv("USE_VERTEX_AI", "False").lower() == "true"
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        
        if self.use_openai and OPENAI_AVAILABLE and self.openai_api_key:
            openai.api_key = self.openai_api_key
            logger.info("OpenAI API initialized for chatbot")
        else:
            self.use_openai = False
        
        if self.use_vertex_ai and VERTEX_AI_AVAILABLE and self.project_id:
            try:
                aiplatform.init(project=self.project_id)
                logger.info("Vertex AI initialized for chatbot")
            except Exception as e:
                logger.warning(f"Failed to initialize Vertex AI: {e}")
                self.use_vertex_ai = False
        
        # Fallback responses for when no AI service is available
        self.fallback_responses = [
            "I understand you're asking about the legal document. Based on the analysis, this appears to be a standard legal agreement.",
            "The document contains several clauses that should be reviewed carefully. I recommend consulting with a legal professional for specific questions.",
            "This legal document includes terms and conditions that govern the relationship between the parties involved.",
            "The risk assessment shows various levels of potential concerns that should be addressed before signing.",
            "I can help explain the general structure of the document, but for legal advice, please consult with an attorney."
        ]
    
    async def get_response(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Get a response from the chatbot
        """
        try:
            if self.use_openai:
                return await self._get_openai_response(message, document_context)
            elif self.use_vertex_ai:
                return await self._get_vertex_ai_response(message, document_context)
            else:
                return await self._get_fallback_response(message, document_context)
                
        except Exception as e:
            logger.error(f"Error getting chatbot response: {e}")
            return {
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again later.",
                "confidence": 0.1
            }
    
    async def _get_openai_response(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Get response using OpenAI API
        """
        try:
            # Build the prompt
            system_prompt = """You are a helpful legal document assistant. You help users understand legal documents by:
1. Explaining legal terms in simple language
2. Identifying potential risks and concerns
3. Answering questions about document content
4. Providing general guidance (but always recommend consulting a lawyer for legal advice)

Always be helpful, accurate, and remind users that you provide general information only, not legal advice."""
            
            user_prompt = message
            if document_context:
                user_prompt = f"Document context: {document_context}\n\nUser question: {message}"
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
            )
            
            return {
                "response": response.choices[0].message.content.strip(),
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"OpenAI chatbot failed: {e}")
            return await self._get_fallback_response(message, document_context)
    
    async def _get_vertex_ai_response(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Get response using Vertex AI
        """
        try:
            # This is a placeholder for Vertex AI implementation
            # In a real implementation, you would use the Vertex AI SDK
            logger.info("Vertex AI chatbot not fully implemented, using fallback")
            return await self._get_fallback_response(message, document_context)
            
        except Exception as e:
            logger.error(f"Vertex AI chatbot failed: {e}")
            return await self._get_fallback_response(message, document_context)
    
    async def _get_fallback_response(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Get a fallback response when AI services are not available
        """
        try:
            # Simple keyword-based responses
            message_lower = message.lower()
            
            # Check for common question patterns
            if any(word in message_lower for word in ['what', 'explain', 'mean', 'meaning']):
                response = "I can help explain legal terms and concepts. Based on the document analysis, I recommend reviewing the risk assessment and summaries provided. For specific legal questions, please consult with a qualified attorney."
            
            elif any(word in message_lower for word in ['risk', 'dangerous', 'safe', 'concern']):
                response = "The risk assessment shows various levels of potential concerns in the document. High-risk clauses are highlighted in red, medium-risk in orange, and low-risk in green. Please review these carefully before making any decisions."
            
            elif any(word in message_lower for word in ['sign', 'agree', 'accept', 'contract']):
                response = "Before signing any legal document, it's important to understand all terms and conditions. Review the summaries provided and consider the risk assessment. I strongly recommend consulting with a legal professional before signing."
            
            elif any(word in message_lower for word in ['clause', 'section', 'paragraph', 'term']):
                response = "The document has been segmented into clauses for easier analysis. Each clause has been analyzed for risk factors and summarized. You can review the detailed breakdown in the document analysis."
            
            elif any(word in message_lower for word in ['liability', 'damages', 'responsible']):
                response = "Liability and responsibility clauses are important to understand. These determine who is responsible for what and under what circumstances. The risk assessment will highlight any concerning liability terms."
            
            elif any(word in message_lower for word in ['terminate', 'end', 'cancel', 'breach']):
                response = "Termination and breach clauses define when and how the agreement can be ended. These are often high-risk areas that should be carefully reviewed. Check the risk assessment for any concerning termination terms."
            
            elif any(word in message_lower for word in ['payment', 'fee', 'cost', 'money']):
                response = "Payment terms specify when, how much, and under what conditions payments are due. Review these carefully as they often contain important deadlines and penalties."
            
            elif any(word in message_lower for word in ['confidential', 'secret', 'private', 'proprietary']):
                response = "Confidentiality clauses protect sensitive information. These are important for maintaining privacy and protecting business interests. Review these terms carefully."
            
            else:
                # Use a random fallback response
                import random
                response = random.choice(self.fallback_responses)
            
            # Add context if available
            if document_context:
                response += f"\n\nBased on the document context: {document_context[:200]}..."
            
            return {
                "response": response,
                "confidence": 0.6
            }
            
        except Exception as e:
            logger.error(f"Fallback response failed: {e}")
            return {
                "response": "I'm here to help with your legal document questions. Please feel free to ask about specific terms, clauses, or concerns you have about the document.",
                "confidence": 0.3
            }
    
    async def get_suggested_questions(self, document_context: str = None) -> List[str]:
        """
        Get suggested questions based on the document context
        """
        try:
            suggested_questions = [
                "What are the main risks in this document?",
                "Can you explain the liability clauses?",
                "What happens if I breach this agreement?",
                "Are there any automatic termination clauses?",
                "What are my payment obligations?",
                "What confidential information is protected?",
                "Can you explain the key terms in simple language?",
                "What should I be most concerned about?",
                "Are there any unusual or risky clauses?",
                "What are my rights under this agreement?"
            ]
            
            # Filter questions based on document context if available
            if document_context:
                context_lower = document_context.lower()
                filtered_questions = []
                
                for question in suggested_questions:
                    question_lower = question.lower()
                    
                    # Check if question is relevant to the document
                    if any(word in context_lower for word in ['liability', 'damages']) and 'liability' in question_lower:
                        filtered_questions.append(question)
                    elif any(word in context_lower for word in ['payment', 'fee']) and 'payment' in question_lower:
                        filtered_questions.append(question)
                    elif any(word in context_lower for word in ['confidential', 'secret']) and 'confidential' in question_lower:
                        filtered_questions.append(question)
                    elif any(word in context_lower for word in ['terminate', 'breach']) and any(word in question_lower for word in ['terminate', 'breach']):
                        filtered_questions.append(question)
                    else:
                        filtered_questions.append(question)
                
                return filtered_questions[:5]  # Return top 5 relevant questions
            
            return suggested_questions[:5]
            
        except Exception as e:
            logger.error(f"Error getting suggested questions: {e}")
            return [
                "What are the main risks in this document?",
                "Can you explain the key terms?",
                "What should I be concerned about?",
                "Are there any unusual clauses?",
                "What are my main obligations?"
            ]
