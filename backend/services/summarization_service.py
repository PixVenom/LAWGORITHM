import os
import logging
from typing import Dict, Any
import asyncio

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)

class SummarizationService:
    def __init__(self):
        self.use_openai = os.getenv("USE_OPENAI", "False").lower() == "true"
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.use_openai and OPENAI_AVAILABLE and self.openai_api_key:
            openai.api_key = self.openai_api_key
            logger.info("OpenAI API initialized")
        else:
            self.use_openai = False
        
        # Initialize local models
        self.models = {}
        if TRANSFORMERS_AVAILABLE:
            self._load_models()
    
    def _load_models(self):
        """
        Load local summarization models
        """
        try:
            # Load a general summarization model
            self.models['general'] = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                tokenizer="facebook/bart-large-cnn",
                max_length=512,
                min_length=50
            )
            logger.info("BART summarization model loaded")
            
            # Load a legal-specific model if available
            try:
                self.models['legal'] = pipeline(
                    "summarization",
                    model="google/pegasus-large",
                    tokenizer="google/pegasus-large",
                    max_length=512,
                    min_length=50
                )
                logger.info("Pegasus summarization model loaded")
            except Exception as e:
                logger.warning(f"Failed to load Pegasus model: {e}")
                self.models['legal'] = self.models['general']
                
        except Exception as e:
            logger.error(f"Failed to load summarization models: {e}")
            self.models = {}
    
    async def generate_summaries(self, text: str) -> Dict[str, str]:
        """
        Generate three levels of summaries: ELI5, Plain Language, and Detailed
        """
        try:
            if not text.strip():
                return {
                    "eli5": "No text to summarize",
                    "plain_language": "No text to summarize",
                    "detailed": "No text to summarize"
                }
            
            # Run summarization in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            
            if self.use_openai:
                summaries = await loop.run_in_executor(
                    None, self._generate_with_openai, text
                )
            else:
                summaries = await loop.run_in_executor(
                    None, self._generate_with_local_models, text
                )
            
            return summaries
            
        except Exception as e:
            logger.error(f"Error generating summaries: {e}")
            return {
                "eli5": f"Error generating summary: {str(e)}",
                "plain_language": f"Error generating summary: {str(e)}",
                "detailed": f"Error generating summary: {str(e)}"
            }
    
    def _generate_with_openai(self, text: str) -> Dict[str, str]:
        """
        Generate summaries using OpenAI API
        """
        try:
            # Truncate text if too long
            max_chars = 4000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            # ELI5 Summary
            eli5_prompt = f"""
            Explain this legal document like I'm 5 years old. Use simple words and analogies. 
            Focus on what the person can and cannot do, and what happens if they break the rules.
            
            Document: {text}
            """
            
            eli5_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": eli5_prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            # Plain Language Summary
            plain_prompt = f"""
            Summarize this legal document in plain, everyday language. Remove legal jargon and 
            explain what it means in simple terms that anyone can understand.
            
            Document: {text}
            """
            
            plain_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": plain_prompt}],
                max_tokens=400,
                temperature=0.5
            )
            
            # Detailed Summary
            detailed_prompt = f"""
            Provide a comprehensive summary of this legal document. Include all key terms, 
            conditions, obligations, and important details while maintaining accuracy.
            
            Document: {text}
            """
            
            detailed_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": detailed_prompt}],
                max_tokens=600,
                temperature=0.3
            )
            
            return {
                "eli5": eli5_response.choices[0].message.content.strip(),
                "plain_language": plain_response.choices[0].message.content.strip(),
                "detailed": detailed_response.choices[0].message.content.strip()
            }
            
        except Exception as e:
            logger.error(f"OpenAI summarization failed: {e}")
            return self._generate_with_local_models(text)
    
    def _generate_with_local_models(self, text: str) -> Dict[str, str]:
        """
        Generate summaries using local models
        """
        try:
            # Truncate text if too long for the model
            max_chars = 2000
            if len(text) > max_chars:
                text = text[:max_chars] + "..."
            
            # Use the best available model
            model = self.models.get('legal', self.models.get('general'))
            
            if not model:
                return self._generate_fallback_summaries(text)
            
            # Generate base summary
            summary_result = model(text, max_length=200, min_length=50, do_sample=False)
            base_summary = summary_result[0]['summary_text']
            
            # Create different levels of summaries
            eli5 = self._create_eli5_summary(base_summary)
            plain_language = self._create_plain_language_summary(base_summary)
            detailed = self._create_detailed_summary(text, base_summary)
            
            return {
                "eli5": eli5,
                "plain_language": plain_language,
                "detailed": detailed
            }
            
        except Exception as e:
            logger.error(f"Local model summarization failed: {e}")
            return self._generate_fallback_summaries(text)
    
    def _create_eli5_summary(self, base_summary: str) -> str:
        """
        Create an ELI5 version of the summary
        """
        # Simple transformation to make it more child-friendly
        eli5 = base_summary.lower()
        
        # Replace legal terms with simple explanations
        replacements = {
            'agreement': 'promise',
            'contract': 'deal',
            'obligation': 'thing you must do',
            'liability': 'responsibility',
            'breach': 'breaking the promise',
            'terminate': 'end',
            'party': 'person or company',
            'shall': 'will',
            'must': 'have to',
            'prohibited': 'not allowed',
            'confidential': 'secret',
            'indemnify': 'protect from harm',
            'damages': 'money for problems caused'
        }
        
        for legal_term, simple_term in replacements.items():
            eli5 = eli5.replace(legal_term, simple_term)
        
        return f"Think of this like a promise between people. {eli5.capitalize()}"
    
    def _create_plain_language_summary(self, base_summary: str) -> str:
        """
        Create a plain language version of the summary
        """
        # Remove complex legal jargon and make it more readable
        plain = base_summary
        
        # Replace complex terms with simpler ones
        replacements = {
            'hereinafter': 'from now on',
            'whereas': 'since',
            'notwithstanding': 'despite',
            'pursuant to': 'according to',
            'in accordance with': 'following',
            'subject to': 'depending on',
            'provided that': 'as long as',
            'in the event that': 'if',
            'shall be deemed': 'will be considered',
            'without prejudice to': 'without affecting'
        }
        
        for complex_term, simple_term in replacements.items():
            plain = plain.replace(complex_term, simple_term)
        
        return plain
    
    def _create_detailed_summary(self, original_text: str, base_summary: str) -> str:
        """
        Create a detailed summary with more information
        """
        # Extract key information from the original text
        key_points = []
        
        # Look for important legal elements
        if 'shall' in original_text.lower():
            key_points.append("Contains obligations and requirements")
        if 'liability' in original_text.lower():
            key_points.append("Addresses liability and responsibility")
        if 'terminate' in original_text.lower():
            key_points.append("Includes termination conditions")
        if 'confidential' in original_text.lower():
            key_points.append("Contains confidentiality provisions")
        if 'payment' in original_text.lower() or 'fee' in original_text.lower():
            key_points.append("Includes payment terms")
        
        detailed = base_summary
        if key_points:
            detailed += "\n\nKey Elements:\n" + "\n".join(f"• {point}" for point in key_points)
        
        return detailed
    
    def _generate_fallback_summaries(self, text: str) -> Dict[str, str]:
        """
        Generate basic summaries when models are not available
        """
        # Simple extractive summarization
        sentences = text.split('.')
        if len(sentences) <= 3:
            summary = text
        else:
            # Take first few sentences as summary
            summary = '. '.join(sentences[:3]) + '.'
        
        return {
            "eli5": f"This document is about rules and promises. {summary}",
            "plain_language": summary,
            "detailed": f"Document Summary: {summary}\n\nFull Text: {text[:500]}..."
        }
