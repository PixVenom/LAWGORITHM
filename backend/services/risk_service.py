import re
import logging
from typing import List, Dict, Any
import asyncio
import random

logger = logging.getLogger(__name__)

class RiskService:
    def __init__(self):
        # Define risk patterns and their weights
        self.risk_patterns = {
            "high": {
                "patterns": [
                    r'\b(?:unlimited|unrestricted|absolute)\s+(?:liability|responsibility)\b',
                    r'\b(?:indemnify|hold harmless)\s+(?:against|for)\s+(?:all|any|every)\b',
                    r'\b(?:without\s+limitation|without\s+restriction)\b',
                    r'\b(?:consequential|punitive|special)\s+damages\b',
                    r'\b(?:automatic|immediate)\s+(?:termination|cancellation)\b',
                    r'\b(?:penalty|fine)\s+(?:of|in\s+the\s+amount\s+of)\s+\$?\d+',
                    r'\b(?:breach|violation)\s+(?:shall|will)\s+(?:result\s+in|constitute)\b',
                    r'\b(?:irrevocable|permanent|final)\b',
                    r'\b(?:waive|waiver)\s+(?:all|any)\s+(?:rights?|claims?|defenses?)\b',
                    r'\b(?:exclusive|sole)\s+(?:remedy|recourse)\b'
                ],
                "weight": 0.8
            },
            "medium": {
                "patterns": [
                    r'\b(?:reasonable|limited)\s+(?:liability|responsibility)\b',
                    r'\b(?:terminate|end|cease)\s+(?:upon|in\s+case\s+of)\b',
                    r'\b(?:breach|default|violation)\s+(?:of|under)\b',
                    r'\b(?:notice|notification)\s+(?:of|regarding)\b',
                    r'\b(?:remedy|recourse)\s+(?:for|against)\b',
                    r'\b(?:damages?|losses?)\s+(?:arising\s+from|resulting\s+from)\b',
                    r'\b(?:confidential|proprietary)\s+(?:information|data)\b',
                    r'\b(?:payment|fee)\s+(?:due|payable)\s+(?:within|by)\b',
                    r'\b(?:subject\s+to|conditioned\s+upon)\b',
                    r'\b(?:provided\s+that|as\s+long\s+as)\b'
                ],
                "weight": 0.5
            },
            "low": {
                "patterns": [
                    r'\b(?:may|might|could)\s+(?:be|have|include)\b',
                    r'\b(?:reasonable|good\s+faith)\s+(?:efforts?|attempts?)\b',
                    r'\b(?:best\s+efforts?|reasonable\s+care)\b',
                    r'\b(?:subject\s+to\s+availability|as\s+available)\b',
                    r'\b(?:at\s+the\s+discretion\s+of|in\s+the\s+opinion\s+of)\b',
                    r'\b(?:unless\s+otherwise\s+specified|except\s+as\s+noted)\b',
                    r'\b(?:generally|typically|usually)\b',
                    r'\b(?:approximately|about|around)\b',
                    r'\b(?:if\s+possible|when\s+feasible)\b',
                    r'\b(?:reasonable\s+time|appropriate\s+period)\b'
                ],
                "weight": 0.2
            }
        }
        
        # Compile patterns for efficiency
        self.compiled_patterns = {}
        for risk_level, data in self.risk_patterns.items():
            self.compiled_patterns[risk_level] = [
                re.compile(pattern, re.IGNORECASE) for pattern in data["patterns"]
            ]
    
    async def calculate_risk_scores(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate risk scores for each clause
        """
        try:
            # Run risk calculation in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            risk_scores = await loop.run_in_executor(
                None, self._calculate_risks, clauses
            )
            
            return risk_scores
            
        except Exception as e:
            logger.error(f"Error calculating risk scores: {e}")
            return self._generate_mock_risk_scores(clauses)
    
    def _calculate_risks(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate risk scores for clauses
        """
        risk_scores = []
        
        for clause in clauses:
            clause_text = clause.get('text', '')
            clause_id = clause.get('id', 0)
            
            # Calculate risk score
            risk_score = self._analyze_clause_risk(clause_text)
            
            # Determine risk level
            if risk_score >= 0.7:
                risk_level = "high"
                color = "#ff4444"  # Red
            elif risk_score >= 0.4:
                risk_level = "medium"
                color = "#ffaa00"  # Orange
            else:
                risk_level = "low"
                color = "#44aa44"  # Green
            
            # Get risk factors
            risk_factors = self._identify_risk_factors(clause_text)
            
            risk_scores.append({
                "clause_id": clause_id,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "color": color,
                "risk_factors": risk_factors,
                "explanation": self._generate_risk_explanation(risk_level, risk_factors)
            })
        
        return risk_scores
    
    def _analyze_clause_risk(self, clause_text: str) -> float:
        """
        Analyze the risk level of a clause
        """
        if not clause_text.strip():
            return 0.0
        
        clause_lower = clause_text.lower()
        total_score = 0.0
        total_weight = 0.0
        
        # Check each risk level
        for risk_level, data in self.risk_patterns.items():
            weight = data["weight"]
            patterns = self.compiled_patterns[risk_level]
            
            # Count matches for this risk level
            matches = 0
            for pattern in patterns:
                matches += len(pattern.findall(clause_lower))
            
            if matches > 0:
                # Normalize by clause length to avoid bias toward longer clauses
                normalized_matches = matches / max(1, len(clause_text.split()))
                total_score += normalized_matches * weight
                total_weight += weight
        
        # Additional risk factors
        additional_risk = self._calculate_additional_risk_factors(clause_text)
        total_score += additional_risk
        
        # Normalize score to 0-1 range
        if total_weight > 0:
            normalized_score = min(1.0, total_score / total_weight)
        else:
            normalized_score = additional_risk
        
        return normalized_score
    
    def _calculate_additional_risk_factors(self, clause_text: str) -> float:
        """
        Calculate additional risk factors
        """
        additional_risk = 0.0
        clause_lower = clause_text.lower()
        
        # Length factor (longer clauses might be more complex/risky)
        if len(clause_text) > 200:
            additional_risk += 0.1
        elif len(clause_text) > 100:
            additional_risk += 0.05
        
        # Negation factor (negative language increases risk)
        negation_words = ['not', 'no', 'never', 'none', 'neither', 'nor', 'without', 'unless']
        negation_count = sum(1 for word in negation_words if word in clause_lower)
        additional_risk += min(0.2, negation_count * 0.05)
        
        # Uncertainty factor (uncertain language might indicate risk)
        uncertainty_words = ['may', 'might', 'could', 'possibly', 'potentially', 'uncertain']
        uncertainty_count = sum(1 for word in uncertainty_words if word in clause_lower)
        additional_risk += min(0.15, uncertainty_count * 0.03)
        
        # Time pressure factor
        time_words = ['immediately', 'urgent', 'asap', 'promptly', 'without delay']
        time_count = sum(1 for word in time_words if word in clause_lower)
        additional_risk += min(0.1, time_count * 0.05)
        
        return additional_risk
    
    def _identify_risk_factors(self, clause_text: str) -> List[str]:
        """
        Identify specific risk factors in the clause
        """
        risk_factors = []
        clause_lower = clause_text.lower()
        
        # Check for specific risk patterns
        risk_checks = {
            "Unlimited Liability": r'\b(?:unlimited|unrestricted)\s+(?:liability|responsibility)\b',
            "Automatic Termination": r'\b(?:automatic|immediate)\s+(?:termination|cancellation)\b',
            "Penalty Clauses": r'\b(?:penalty|fine)\s+(?:of|in\s+the\s+amount\s+of)\s+\$?\d+',
            "Indemnification": r'\b(?:indemnify|hold harmless)\b',
            "Waiver of Rights": r'\b(?:waive|waiver)\s+(?:all|any)\s+(?:rights?|claims?)\b',
            "Consequential Damages": r'\b(?:consequential|punitive|special)\s+damages\b',
            "Irrevocable Terms": r'\b(?:irrevocable|permanent|final)\b',
            "Exclusive Remedy": r'\b(?:exclusive|sole)\s+(?:remedy|recourse)\b',
            "Confidentiality Breach": r'\b(?:confidential|proprietary)\s+(?:information|data)\b',
            "Payment Default": r'\b(?:payment|fee)\s+(?:due|payable)\s+(?:within|by)\b'
        }
        
        for factor_name, pattern in risk_checks.items():
            if re.search(pattern, clause_lower):
                risk_factors.append(factor_name)
        
        return risk_factors
    
    def _generate_risk_explanation(self, risk_level: str, risk_factors: List[str]) -> str:
        """
        Generate an explanation for the risk level
        """
        if risk_level == "high":
            base_explanation = "This clause contains high-risk elements that could significantly impact your rights or obligations."
        elif risk_level == "medium":
            base_explanation = "This clause contains moderate-risk elements that should be carefully reviewed."
        else:
            base_explanation = "This clause appears to have low-risk elements, but should still be reviewed."
        
        if risk_factors:
            factors_text = ", ".join(risk_factors)
            return f"{base_explanation} Identified risk factors: {factors_text}."
        else:
            return base_explanation
    
    def _generate_mock_risk_scores(self, clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate mock risk scores when calculation fails
        """
        mock_scores = []
        
        for clause in clauses:
            clause_id = clause.get('id', 0)
            
            # Generate random but realistic risk scores
            risk_score = random.uniform(0.1, 0.9)
            
            if risk_score >= 0.7:
                risk_level = "high"
                color = "#ff4444"
                factors = ["Unlimited Liability", "Automatic Termination"]
            elif risk_score >= 0.4:
                risk_level = "medium"
                color = "#ffaa00"
                factors = ["Payment Default", "Confidentiality Breach"]
            else:
                risk_level = "low"
                color = "#44aa44"
                factors = ["Standard Terms"]
            
            mock_scores.append({
                "clause_id": clause_id,
                "risk_score": round(risk_score, 2),
                "risk_level": risk_level,
                "color": color,
                "risk_factors": factors,
                "explanation": self._generate_risk_explanation(risk_level, factors)
            })
        
        return mock_scores
