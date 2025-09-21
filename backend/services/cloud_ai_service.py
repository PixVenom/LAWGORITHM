import os
import logging
from typing import Dict, Any, List
import asyncio

try:
    import vertexai
    from vertexai.language_models import TextGenerationModel
    from vertexai.generative_models import GenerativeModel
    GOOGLE_VERTEX_AI_AVAILABLE = True
except ImportError:
    GOOGLE_VERTEX_AI_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

class CloudAIService:
    def __init__(self):
        self.use_vertex_ai = os.getenv("USE_VERTEX_AI", "False").lower() == "true"
        self.use_openai = os.getenv("USE_OPENAI", "False").lower() == "true"
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize Vertex AI
        if self.use_vertex_ai and GOOGLE_VERTEX_AI_AVAILABLE and self.project_id:
            try:
                vertexai.init(project=self.project_id)
                self.vertex_model = TextGenerationModel.from_pretrained("text-bison@001")
                self.gemini_model = GenerativeModel("gemini-pro")
                logger.info("Vertex AI initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Vertex AI: {e}")
                self.use_vertex_ai = False
        
        # Initialize OpenAI
        if self.use_openai and OPENAI_AVAILABLE and self.openai_api_key:
            try:
                openai.api_key = self.openai_api_key
                logger.info("OpenAI API initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI: {e}")
                self.use_openai = False
    
    async def generate_legal_summary(self, text: str, summary_type: str) -> Dict[str, Any]:
        """
        Generate legal summary using cloud AI services
        """
        try:
            if self.use_vertex_ai:
                return await self._generate_with_vertex_ai(text, summary_type)
            elif self.use_openai:
                return await self._generate_with_openai(text, summary_type)
            else:
                return await self._generate_fallback(text, summary_type)
                
        except Exception as e:
            logger.error(f"Error generating legal summary: {e}")
            return await self._generate_fallback(text, summary_type)
    
    async def _generate_with_vertex_ai(self, text: str, summary_type: str) -> Dict[str, Any]:
        """
        Generate summary using Vertex AI
        """
        try:
            # Truncate text if too long
            max_chars = 4000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            if summary_type == "eli5":
                prompt = f"""
                Explain this legal document like I'm 5 years old. Use simple words and analogies.
                Focus on what the person can and cannot do, and what happens if they break the rules.
                Keep it under 200 words.
                
                Document: {text}
                """
            elif summary_type == "plain":
                prompt = f"""
                Summarize this legal document in plain, everyday language. Remove legal jargon.
                Explain what it means in simple terms that anyone can understand.
                Keep it under 300 words.
                
                Document: {text}
                """
            else:  # detailed
                prompt = f"""
                Provide a comprehensive summary of this legal document. Include all key terms,
                conditions, obligations, and important details while maintaining accuracy.
                Keep it under 500 words.
                
                Document: {text}
                """
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.vertex_model.predict(
                    prompt,
                    max_output_tokens=1024,
                    temperature=0.7
                )
            )
            
            return {
                "summary": response.text.strip(),
                "method": "Vertex AI (Text-Bison)",
                "confidence": 0.9,
                "model": "text-bison@001"
            }
            
        except Exception as e:
            logger.error(f"Vertex AI generation failed: {e}")
            if self.use_openai:
                return await self._generate_with_openai(text, summary_type)
            else:
                return await self._generate_fallback(text, summary_type)
    
    async def _generate_with_openai(self, text: str, summary_type: str) -> Dict[str, Any]:
        """
        Generate summary using OpenAI API
        """
        try:
            # Truncate text if too long
            max_chars = 4000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            if summary_type == "eli5":
                system_prompt = "You are a helpful assistant that explains legal documents in simple terms for children."
                user_prompt = f"Explain this legal document like I'm 5 years old: {text}"
            elif summary_type == "plain":
                system_prompt = "You are a legal assistant that explains documents in plain language."
                user_prompt = f"Summarize this legal document in plain language: {text}"
            else:
                system_prompt = "You are a legal expert that provides comprehensive document analysis."
                user_prompt = f"Provide a detailed summary of this legal document: {text}"
            
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
                "summary": response.choices[0].message.content.strip(),
                "method": "OpenAI GPT-3.5-turbo",
                "confidence": 0.9,
                "model": "gpt-3.5-turbo"
            }
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return await self._generate_fallback(text, summary_type)
    
    async def _generate_fallback(self, text: str, summary_type: str) -> Dict[str, Any]:
        """
        Fallback summary generation using simple text processing
        """
        try:
            # Simple extractive summarization
            sentences = text.split('.')
            if len(sentences) <= 3:
                summary = text
            else:
                # Take first few sentences as summary
                summary = '. '.join(sentences[:3]) + '.'
            
            if summary_type == "eli5":
                summary = f"This document is about rules and promises. {summary}"
            elif summary_type == "plain":
                summary = summary
            else:
                summary = f"Document Summary: {summary}\n\nKey Points: This document contains important legal terms and conditions."
            
            return {
                "summary": summary,
                "method": "Fallback (Simple Processing)",
                "confidence": 0.5,
                "model": "fallback"
            }
            
        except Exception as e:
            logger.error(f"Fallback generation failed: {e}")
            return {
                "summary": "Unable to generate summary at this time.",
                "method": "Error",
                "confidence": 0.0,
                "model": "error"
            }
    
    async def generate_chat_response(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Generate chat response using cloud AI
        """
        try:
            if self.use_vertex_ai:
                return await self._chat_with_vertex_ai(message, document_context)
            elif self.use_openai:
                return await self._chat_with_openai(message, document_context)
            else:
                return await self._chat_fallback(message, document_context)
                
        except Exception as e:
            logger.error(f"Error generating chat response: {e}")
            return await self._chat_fallback(message, document_context)
    
    async def _chat_with_vertex_ai(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Generate chat response using Vertex AI
        """
        try:
            context = f"Document context: {document_context}\n\n" if document_context else ""
            prompt = f"""
            You are a helpful legal document assistant. Answer the user's question about the legal document.
            Be helpful, accurate, and always recommend consulting a lawyer for legal advice.
            
            {context}User question: {message}
            """
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.vertex_model.predict(
                    prompt,
                    max_output_tokens=500,
                    temperature=0.7
                )
            )
            
            return {
                "response": response.text.strip(),
                "confidence": 0.9,
                "method": "Vertex AI Chat"
            }
            
        except Exception as e:
            logger.error(f"Vertex AI chat failed: {e}")
            return await self._chat_fallback(message, document_context)
    
    async def _chat_with_openai(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Generate chat response using OpenAI
        """
        try:
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
                "confidence": 0.9,
                "method": "OpenAI Chat"
            }
            
        except Exception as e:
            logger.error(f"OpenAI chat failed: {e}")
            return await self._chat_fallback(message, document_context)
    
    async def _chat_fallback(self, message: str, document_context: str = None) -> Dict[str, Any]:
        """
        Fallback chat response
        """
        # Simple keyword-based responses
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['what', 'explain', 'mean', 'meaning']):
            response = "I can help explain legal terms and concepts. Based on the document analysis, I recommend reviewing the risk assessment and summaries provided. For specific legal questions, please consult with a qualified attorney."
        elif any(word in message_lower for word in ['risk', 'dangerous', 'safe', 'concern']):
            response = "The risk assessment shows various levels of potential concerns in the document. High-risk clauses are highlighted in red, medium-risk in orange, and low-risk in green. Please review these carefully before making any decisions."
        elif any(word in message_lower for word in ['sign', 'agree', 'accept', 'contract']):
            response = "Before signing any legal document, it's important to understand all terms and conditions. Review the summaries provided and consider the risk assessment. I strongly recommend consulting with a legal professional before signing."
        else:
            response = "I'm here to help with your legal document questions. Please feel free to ask about specific terms, clauses, or concerns you have about the document."
        
        return {
            "response": response,
            "confidence": 0.6,
            "method": "Fallback Chat"
        }
    
    async def analyze_legal_risks(self, text: str) -> Dict[str, Any]:
        """
        Analyze legal risks using AI
        """
        try:
            if self.use_vertex_ai:
                return await self._analyze_risks_with_vertex_ai(text)
            elif self.use_openai:
                return await self._analyze_risks_with_openai(text)
            else:
                return await self._analyze_risks_fallback(text)
                
        except Exception as e:
            logger.error(f"Error analyzing legal risks: {e}")
            return await self._analyze_risks_fallback(text)
    
    async def _analyze_risks_with_vertex_ai(self, text: str) -> Dict[str, Any]:
        """
        Analyze risks using Vertex AI
        """
        try:
            prompt = f"""
            Analyze this legal document for potential risks and concerns. Identify:
            1. High-risk clauses (unlimited liability, automatic termination, etc.)
            2. Medium-risk clauses (payment terms, confidentiality, etc.)
            3. Low-risk clauses (standard terms, etc.)
            
            Provide a JSON response with risk levels and explanations.
            
            Document: {text[:2000]}
            """
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.vertex_model.predict(
                    prompt,
                    max_output_tokens=800,
                    temperature=0.3
                )
            )
            
            return {
                "analysis": response.text.strip(),
                "method": "Vertex AI Risk Analysis",
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"Vertex AI risk analysis failed: {e}")
            return await self._analyze_risks_fallback(text)
    
    async def _analyze_risks_with_openai(self, text: str) -> Dict[str, Any]:
        """
        Analyze risks using OpenAI
        """
        try:
            prompt = f"""
            Analyze this legal document for potential risks and concerns. Identify high-risk, medium-risk, and low-risk clauses.
            Provide specific examples and explanations for each risk level.
            
            Document: {text[:2000]}
            """
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a legal risk analyst. Provide detailed risk assessments."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=600,
                    temperature=0.3
                )
            )
            
            return {
                "analysis": response.choices[0].message.content.strip(),
                "method": "OpenAI Risk Analysis",
                "confidence": 0.9
            }
            
        except Exception as e:
            logger.error(f"OpenAI risk analysis failed: {e}")
            return await self._analyze_risks_fallback(text)
    
    async def _analyze_risks_fallback(self, text: str) -> Dict[str, Any]:
        """
        Fallback risk analysis
        """
        # Simple keyword-based risk analysis
        high_risk_keywords = ['unlimited', 'automatic', 'penalty', 'irrevocable', 'waive']
        medium_risk_keywords = ['liability', 'damages', 'breach', 'terminate', 'confidential']
        low_risk_keywords = ['reasonable', 'standard', 'normal', 'typical']
        
        text_lower = text.lower()
        
        high_risks = [word for word in high_risk_keywords if word in text_lower]
        medium_risks = [word for word in medium_risk_keywords if word in text_lower]
        low_risks = [word for word in low_risk_keywords if word in text_lower]
        
        analysis = f"""
        Risk Analysis:
        - High Risk Factors: {', '.join(high_risks) if high_risks else 'None identified'}
        - Medium Risk Factors: {', '.join(medium_risks) if medium_risks else 'None identified'}
        - Low Risk Factors: {', '.join(low_risks) if low_risks else 'None identified'}
        
        Please review the document carefully and consult with a legal professional for detailed analysis.
        """
        
        return {
            "analysis": analysis,
            "method": "Fallback Risk Analysis",
            "confidence": 0.5
        }
