"""
Risk Matrix and Operational Impact Evaluator for environments.
"""
from typing import Dict, Any, Tuple

class EnvironmentsRiskMatrixEvaluator:
    """Calculates risk scores and operational impact for environments."""
    @staticmethod
    def calculate_risk(impact_level: str, probability_level: str) -> Tuple[float, str]:
        impact_weights = {"LOW": 1.0, "MODERATE": 2.5, "HIGH": 5.0, "CRITICAL": 10.0}
        prob_weights = {"LOW": 1.0, "MEDIUM": 2.0, "HIGH": 4.0}
        
        w_imp = impact_weights.get(impact_level.upper(), 2.5)
        w_prob = prob_weights.get(probability_level.upper(), 2.0)
        
        score = round(w_imp * w_prob * 2.5, 2)
        if score >= 60.0:
            category = "HIGH_RISK"
        elif score >= 25.0:
            category = "MEDIUM_RISK"
        else:
            category = "LOW_RISK"
            
        return score, category
