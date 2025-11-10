"""
Feedback Handler Module
Collects and processes human feedback on property analyses
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackHandler:
    """Handles human feedback and corrections to analysis"""

    def __init__(self):
        """Initialize feedback handler"""
        self.feedback_history: List[Dict[str, Any]] = []
        logger.info("Feedback Handler initialized")

    def submit_feedback(
        self,
        property_address: str,
        feedback_type: str,
        feedback_content: str,
        analyst_name: str = "Anonymous",
        confidence_adjustment: float = 0.0
    ) -> Dict[str, Any]:
        """
        Submit feedback on an analysis

        Args:
            property_address: Property being analyzed
            feedback_type: Type of feedback (correction, clarification, approval, rejection)
            feedback_content: Detailed feedback
            analyst_name: Name of analyst providing feedback
            confidence_adjustment: Adjustment to analysis confidence (-1.0 to 1.0)

        Returns:
            Feedback submission record
        """
        feedback_record = {
            "id": len(self.feedback_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "property_address": property_address,
            "feedback_type": feedback_type,
            "feedback_content": feedback_content,
            "analyst_name": analyst_name,
            "confidence_adjustment": max(-1.0, min(1.0, confidence_adjustment)),
            "status": "submitted"
        }

        self.feedback_history.append(feedback_record)
        logger.info(f"Feedback submitted for {property_address} by {analyst_name}")

        return feedback_record

    def get_feedback_for_property(self, property_address: str) -> List[Dict[str, Any]]:
        """
        Retrieve all feedback for a property

        Args:
            property_address: Property address to query

        Returns:
            List of feedback records
        """
        return [f for f in self.feedback_history if f["property_address"] == property_address]

    def apply_feedback_to_analysis(
        self,
        analysis: Dict[str, Any],
        feedback_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Apply human feedback adjustments to analysis

        Args:
            analysis: Original analysis result
            feedback_list: List of feedback records

        Returns:
            Adjusted analysis with feedback applied
        """
        adjusted_analysis = analysis.copy()

        if not feedback_list:
            return adjusted_analysis

        # Calculate average confidence adjustment
        total_adjustment = sum(f.get("confidence_adjustment", 0) for f in feedback_list)
        avg_adjustment = total_adjustment / len(feedback_list) if feedback_list else 0

        # Apply adjustment to valuation confidence
        if "valuation" in adjusted_analysis:
            current_confidence = adjusted_analysis["valuation"].get("confidence_score", 0.85)
            adjusted_confidence = max(0.0, min(1.0, current_confidence + avg_adjustment))
            adjusted_analysis["valuation"]["confidence_score"] = adjusted_confidence

        # Add feedback history
        adjusted_analysis["human_feedback"] = {
            "feedback_count": len(feedback_list),
            "confidence_adjustment": avg_adjustment,
            "last_feedback": datetime.now().isoformat(),
            "feedback_summary": [
                {
                    "type": f.get("feedback_type"),
                    "analyst": f.get("analyst_name"),
                    "content": f.get("feedback_content")[:100] + "..." if len(f.get("feedback_content", "")) > 100 else f.get("feedback_content")
                }
                for f in feedback_list
            ]
        }

        logger.info(f"Applied {len(feedback_list)} feedback records to analysis")
        return adjusted_analysis

    def get_feedback_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of all feedback

        Returns:
            Summary of feedback data
        """
        feedback_types = {}
        for feedback in self.feedback_history:
            ftype = feedback.get("feedback_type", "unknown")
            feedback_types[ftype] = feedback_types.get(ftype, 0) + 1

        return {
            "total_feedback": len(self.feedback_history),
            "feedback_by_type": feedback_types,
            "unique_properties": len(set(f["property_address"] for f in self.feedback_history)),
            "unique_analysts": len(set(f["analyst_name"] for f in self.feedback_history))
        }

    def clear_history(self) -> None:
        """Clear all feedback history"""
        self.feedback_history.clear()
        logger.info("Feedback history cleared")
