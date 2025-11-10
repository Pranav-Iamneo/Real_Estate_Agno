"""
Validation Manager Module
Validates analyses and property data before and after human review
"""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class ValidationManager:
    """Manages validation of property analyses"""

    def __init__(self):
        """Initialize validation manager"""
        self.validation_rules = {
            "valuation": self._validate_valuation,
            "investment": self._validate_investment,
            "market": self._validate_market,
            "risk": self._validate_risk
        }
        logger.info("Validation Manager initialized")

    def validate_analysis(self, analysis: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate complete analysis

        Args:
            analysis: Analysis to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check required fields
        required_fields = [
            "analysis_summary",
            "valuation",
            "investment_analysis",
            "market_analysis",
            "risk_assessment"
        ]

        for field in required_fields:
            if field not in analysis:
                issues.append(f"Missing required field: {field}")

        # Run validation rules
        if "valuation" in analysis:
            val_issues = self._validate_valuation(analysis["valuation"])
            issues.extend(val_issues)

        if "investment_analysis" in analysis:
            inv_issues = self._validate_investment(analysis["investment_analysis"])
            issues.extend(inv_issues)

        if "market_analysis" in analysis:
            mkt_issues = self._validate_market(analysis["market_analysis"])
            issues.extend(mkt_issues)

        if "risk_assessment" in analysis:
            risk_issues = self._validate_risk(analysis["risk_assessment"])
            issues.extend(risk_issues)

        is_valid = len(issues) == 0
        logger.info(f"Validation result: {'PASSED' if is_valid else 'FAILED'} with {len(issues)} issues")

        return is_valid, issues

    def _validate_valuation(self, valuation: Dict[str, Any]) -> List[str]:
        """Validate valuation section"""
        issues = []

        if "estimated_value" not in valuation:
            issues.append("Valuation: Missing estimated_value")
        elif not isinstance(valuation["estimated_value"], (int, float)) or valuation["estimated_value"] <= 0:
            issues.append("Valuation: estimated_value must be positive number")

        if "confidence_score" not in valuation:
            issues.append("Valuation: Missing confidence_score")
        elif not (0 <= valuation.get("confidence_score", 0) <= 1):
            issues.append("Valuation: confidence_score must be between 0 and 1")

        return issues

    def _validate_investment(self, investment: Dict[str, Any]) -> List[str]:
        """Validate investment analysis section"""
        issues = []

        if "roi_percentage" not in investment:
            issues.append("Investment: Missing roi_percentage")

        if "investment_score" not in investment:
            issues.append("Investment: Missing investment_score")
        elif not (1 <= investment.get("investment_score", 0) <= 10):
            issues.append("Investment: investment_score must be between 1 and 10")

        if "recommendation" not in investment:
            issues.append("Investment: Missing recommendation")

        return issues

    def _validate_market(self, market: Dict[str, Any]) -> List[str]:
        """Validate market analysis section"""
        issues = []

        if "market_trend" not in market:
            issues.append("Market: Missing market_trend")

        if "comparable_properties" not in market:
            issues.append("Market: Missing comparable_properties")

        return issues

    def _validate_risk(self, risk: Dict[str, Any]) -> List[str]:
        """Validate risk assessment section"""
        issues = []

        required_risks = ["location_risk", "maintenance_risk", "overall_risk"]
        for risk_field in required_risks:
            if risk_field not in risk:
                issues.append(f"Risk: Missing {risk_field}")

        return issues

    def validate_property_input(self, property_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate property input data

        Args:
            property_data: Property data to validate

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Required fields
        required = ["address", "bedrooms", "bathrooms", "sqft", "age_years"]
        for field in required:
            if field not in property_data:
                issues.append(f"Missing required field: {field}")

        # Field validations
        if "bedrooms" in property_data:
            beds = property_data["bedrooms"]
            if not isinstance(beds, int) or beds < 1 or beds > 20:
                issues.append("Bedrooms must be between 1 and 20")

        if "bathrooms" in property_data:
            baths = property_data["bathrooms"]
            if not isinstance(baths, (int, float)) or baths < 0.5 or baths > 20:
                issues.append("Bathrooms must be between 0.5 and 20")

        if "sqft" in property_data:
            sqft = property_data["sqft"]
            if not isinstance(sqft, int) or sqft < 500 or sqft > 1_000_000:
                issues.append("Square footage must be between 500 and 1,000,000")

        if "age_years" in property_data:
            age = property_data["age_years"]
            if not isinstance(age, int) or age < 0 or age > 200:
                issues.append("Age must be between 0 and 200 years")

        # Location validation
        valid_locations = ["downtown", "urban", "suburban", "rural"]
        if "location_type" in property_data and property_data["location_type"] not in valid_locations:
            issues.append(f"Location type must be one of: {', '.join(valid_locations)}")

        # Condition validation
        valid_conditions = ["excellent", "good", "fair", "needs_repair", "poor"]
        if "condition" in property_data and property_data["condition"] not in valid_conditions:
            issues.append(f"Condition must be one of: {', '.join(valid_conditions)}")

        is_valid = len(issues) == 0
        return is_valid, issues

    def get_validation_report(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a detailed validation report

        Args:
            analysis: Analysis to validate

        Returns:
            Detailed validation report
        """
        is_valid, issues = self.validate_analysis(analysis)

        return {
            "is_valid": is_valid,
            "total_issues": len(issues),
            "issues": issues,
            "property": analysis.get("analysis_summary", {}).get("property_name", "Unknown"),
            "validation_timestamp": __import__("datetime").datetime.now().isoformat(),
            "recommendation": "Ready for use" if is_valid else "Needs review"
        }
