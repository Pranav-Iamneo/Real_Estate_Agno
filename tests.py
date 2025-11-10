"""
Real Estate Intelligence System - Pytest Test Suite
10 Essential Test Cases for System Verification
Run with: pytest tests.py -v
"""

import pytest
from utils.calculations import (
    calculate_base_valuation,
    calculate_price_per_sqft,
    calculate_roi,
    calculate_payback_period,
    calculate_risk_level
)
from utils.validators import validate_property_input
from utils.helpers import (
    generate_confidence_score,
    generate_comparable_properties,
    generate_market_trend
)
from mock_analysis import RealEstateAnalysisEngine
from human_intervention.feedback_handler import FeedbackHandler
from human_intervention.validation_manager import ValidationManager


def test_property_valuation_calculation():
    """Test 1: Base property valuation for urban location"""
    property_data = {
        "sqft": 2500,
        "location_type": "urban",
        "neighborhood_rating": "good",
        "condition": "good",
        "age_years": 10
    }
    result = calculate_base_valuation(property_data)

    assert isinstance(result, (int, float))
    assert result > 0
    assert result < 1000000
    print(f"Urban Property Valuation: ${result:,.2f}")


def test_input_validation_accepts_valid_data():
    """Test 2: Validation accepts valid property data"""
    property_data = {
        "address": "123 Main St",
        "bedrooms": 3,
        "bathrooms": 2.0,
        "sqft": 2500,
        "age_years": 10,
        "location_type": "urban",
        "condition": "good",
        "neighborhood_rating": "good"
    }
    is_valid, errors = validate_property_input(property_data)

    assert is_valid is True
    assert len(errors) == 0
    print("Valid property input: ACCEPTED")


def test_input_validation_rejects_invalid_bedrooms():
    """Test 3: Validation rejects invalid bedroom count"""
    property_data = {
        "address": "123 Main St",
        "bedrooms": 50,
        "bathrooms": 2.0,
        "sqft": 2500,
        "age_years": 10
    }
    is_valid, errors = validate_property_input(property_data)

    assert is_valid is False
    assert len(errors) > 0
    print(f"Invalid input rejected: {len(errors)} error(s)")


def test_roi_and_payback_period_calculation():
    """Test 4: ROI percentage and payback period calculations"""
    annual_return = 20000
    valuation = 300000

    roi = calculate_roi(annual_return, valuation)
    payback_period = calculate_payback_period(annual_return, valuation)

    assert isinstance(roi, (int, float))
    assert isinstance(payback_period, (int, float))
    assert roi > 0
    assert payback_period > 0
    print(f"ROI: {roi:.2f}% | Payback Period: {payback_period:.1f} years")


def test_risk_level_assessment_for_property():
    """Test 5: Risk level calculation for different property characteristics"""
    risk_level = calculate_risk_level("urban", "good", 15)

    valid_risks = ["low", "low-moderate", "moderate", "moderate-high", "high"]
    assert risk_level in valid_risks
    print(f"Risk Level: {risk_level}")


def test_confidence_score_generation_within_range():
    """Test 6: Confidence score is within expected range"""
    score = generate_confidence_score(0.82, 0.98)

    assert isinstance(score, float)
    assert 0.82 <= score <= 0.98
    print(f"Confidence Score: {score:.2f}")


def test_complete_property_analysis_pipeline():
    """Test 7: Complete property analysis with mock engine"""
    property_data = {
        "address": "123 Oak Street, Downtown",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "sqft": 2500,
        "age_years": 8,
        "location_type": "urban",
        "condition": "good",
        "neighborhood_rating": "good"
    }

    result = RealEstateAnalysisEngine.analyze_property(property_data)

    assert result["status"] == "success"
    assert "analysis_summary" in result
    assert "valuation" in result
    assert "investment_analysis" in result
    assert "market_analysis" in result
    assert "risk_assessment" in result

    valuation = result["valuation"]["estimated_value"]
    roi = result["investment_analysis"]["roi_percentage"]
    score = result["investment_analysis"]["investment_score"]

    print(f"Analysis Complete: Value=${valuation:,.0f} | ROI={roi:.1f}% | Score={score:.1f}/10")


def test_feedback_submission_and_retrieval():
    """Test 8: Human feedback submission and retrieval"""
    handler = FeedbackHandler()

    feedback = handler.submit_feedback(
        property_address="123 Main St",
        feedback_type="approval",
        feedback_content="Analysis looks good",
        analyst_name="John Doe",
        confidence_adjustment=0.1
    )

    assert feedback["status"] == "submitted"
    assert feedback["analyst_name"] == "John Doe"
    assert feedback["feedback_type"] == "approval"

    feedback_list = handler.get_feedback_for_property("123 Main St")
    assert len(feedback_list) >= 1

    print(f"Feedback submitted and retrieved: {feedback['id']}")


def test_analysis_validation_structure():
    """Test 9: Analysis validation with proper structure"""
    manager = ValidationManager()

    valid_analysis = {
        "analysis_summary": {"property_name": "Test Property"},
        "valuation": {"estimated_value": 300000, "confidence_score": 0.85},
        "investment_analysis": {"roi_percentage": 8.5, "investment_score": 7, "recommendation": "RECOMMENDED"},
        "market_analysis": {"market_trend": "appreciating", "comparable_properties": []},
        "risk_assessment": {"location_risk": "low", "maintenance_risk": "moderate", "overall_risk": "moderate"}
    }

    is_valid, issues = manager.validate_analysis(valid_analysis)

    assert is_valid is True
    assert len(issues) == 0
    print("Analysis validation: PASSED")


def test_market_analysis_and_comparable_generation():
    """Test 10: Market analysis and comparable properties generation"""
    base_price = 300000

    comparables = generate_comparable_properties(base_price, count=3)
    trend = generate_market_trend()

    assert len(comparables) == 3
    assert all("price" in comp for comp in comparables)
    assert all("sqft" in comp for comp in comparables)
    assert trend in ["appreciating", "stable", "declining"]

    print(f"Generated {len(comparables)} comparables | Market Trend: {trend}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
