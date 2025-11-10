"""
Test Suite for Real Estate Intelligence System
10 essential test cases covering core functionality
"""

import pytest
from config import settings
from mock_analysis import RealEstateAnalysisEngine
from utils.validators import validate_property_input
from utils.calculations import (
    calculate_base_valuation,
    calculate_roi,
    calculate_payback_period,
    calculate_future_value,
    calculate_risk_level
)


# ============================================================================
# TEST 1: Valid Property Input Validation
# ============================================================================
def test_valid_property_input():
    """Test that valid property input passes validation"""
    property_data = {
        "address": "123 Main Street",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "sqft": 2500,
        "age_years": 10,
        "location_type": "urban",
        "condition": "good",
        "neighborhood_rating": "good"
    }
    is_valid, errors = validate_property_input(property_data)
    assert is_valid is True
    assert len(errors) == 0


# ============================================================================
# TEST 2: Invalid Property Input Validation
# ============================================================================
def test_invalid_property_input():
    """Test that invalid property input fails validation"""
    property_data = {
        "address": "123 Main Street",
        "bedrooms": 25,  # Beyond max of 20
        "bathrooms": 2.5,
        "sqft": 100,  # Below min of 500
        "age_years": 10,
        "location_type": "urban",
        "condition": "good",
        "neighborhood_rating": "good"
    }
    is_valid, errors = validate_property_input(property_data)
    assert is_valid is False
    assert len(errors) > 0


# ============================================================================
# TEST 3: Base Valuation Calculation
# ============================================================================
def test_base_valuation_calculation():
    """Test property valuation with multipliers"""
    property_data = {
        "sqft": 2000,
        "location_type": "suburban",
        "neighborhood_rating": "average",
        "condition": "fair",
        "age_years": 10
    }
    valuation = calculate_base_valuation(property_data)

    # Expected: 2000 * 150 * 1.0 * 1.0 * 1.0 * 0.8 = 240,000
    expected = 2000 * 150 * 1.0 * 1.0 * 1.0 * 0.8
    assert abs(valuation - expected) < 1


# ============================================================================
# TEST 4: Downtown Location Premium
# ============================================================================
def test_downtown_location_premium():
    """Test that downtown location gets 40% premium"""
    suburban_data = {
        "sqft": 2000,
        "location_type": "suburban",
        "neighborhood_rating": "average",
        "condition": "fair",
        "age_years": 0
    }
    downtown_data = {
        "sqft": 2000,
        "location_type": "downtown",
        "neighborhood_rating": "average",
        "condition": "fair",
        "age_years": 0
    }

    suburban_val = calculate_base_valuation(suburban_data)
    downtown_val = calculate_base_valuation(downtown_data)

    # Downtown should be 40% more (1.4x multiplier)
    assert abs(downtown_val / suburban_val - 1.4) < 0.01


# ============================================================================
# TEST 5: ROI Calculation
# ============================================================================
def test_roi_calculation():
    """Test ROI percentage calculation"""
    roi = calculate_roi(annual_return=25000, valuation=300000)
    expected = (25000 / 300000) * 100
    assert abs(roi - expected) < 0.01


# ============================================================================
# TEST 6: Payback Period Calculation
# ============================================================================
def test_payback_period_calculation():
    """Test payback period in years calculation"""
    payback = calculate_payback_period(valuation=300000, annual_return=25000)
    expected = 300000 / 25000  # 12 years
    assert abs(payback - expected) < 0.01


# ============================================================================
# TEST 7: Future Value Projection (5 Years)
# ============================================================================
def test_future_value_projection():
    """Test 5-year compound growth calculation"""
    future = calculate_future_value(present_value=300000, annual_rate=0.045, years=5)
    expected = 300000 * (1.045 ** 5)
    assert abs(future - expected) < 1


# ============================================================================
# TEST 8: Risk Level Assessment
# ============================================================================
def test_risk_level_assessment():
    """Test risk level calculation for different property types"""
    # Downtown excellent should be low risk
    risk_low = calculate_risk_level("downtown", "excellent", 5)
    assert risk_low in ["low", "low-moderate"]

    # Rural poor should be high risk
    risk_high = calculate_risk_level("rural", "poor", 70)
    assert risk_high in ["moderate-high", "high"]


# ============================================================================
# TEST 9: Mock Analysis Engine - Property Analysis
# ============================================================================
def test_mock_analysis_engine():
    """Test complete property analysis with all required sections"""
    property_data = {
        "address": "123 Main Street",
        "bedrooms": 3,
        "bathrooms": 2.5,
        "sqft": 2500,
        "age_years": 10,
        "location_type": "urban",
        "condition": "good",
        "neighborhood_rating": "good"
    }

    analysis = RealEstateAnalysisEngine.analyze_property(property_data)

    # Verify all key sections exist
    assert "basic_info" in analysis
    assert "valuation" in analysis
    assert "investment_analysis" in analysis
    assert "risk_assessment" in analysis

    # Verify valuation is positive
    assert analysis["valuation"]["estimated_value"] > 0

    # Verify investment score is in valid range
    assert 1 <= analysis["investment_analysis"]["investment_score"] <= 10


# ============================================================================
# TEST 10: Configuration Settings Validation
# ============================================================================
def test_configuration_settings():
    """Test that system configuration is loaded correctly"""
    assert settings.AGENT_MODEL == "gemini-2.0-flash"
    assert settings.AGENT_TEMPERATURE == 0.7
    assert settings.AGENT_MAX_TOKENS == 4096
    assert settings.CURRENCY == "USD"
    assert settings.DB_FILE == "real_estate.db"
    assert isinstance(settings.API_PORT, int)
    assert settings.API_PORT > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
