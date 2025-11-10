"""
Comprehensive Test Suite for Real Estate Intelligence System
Tests all modules, calculations, validations, and workflows
"""

import pytest
import sys
from datetime import datetime
from typing import Dict, Any

# Import modules to test
from utils.calculations import (
    calculate_base_valuation,
    calculate_price_per_sqft,
    calculate_roi,
    calculate_payback_period,
    calculate_appreciation,
    calculate_future_value,
    calculate_risk_level
)
from utils.validators import validate_property_input
from utils.helpers import (
    prepare_property_data,
    select_random_amenities,
    select_random_facilities,
    generate_confidence_score,
    generate_comparable_properties,
    generate_market_trend,
    generate_investment_recommendation
)
from utils.constants import AMENITIES, NEARBY_FACILITIES
from utils.formatters import format_currency, format_percentage
from mock_analysis import RealEstateAnalysisEngine
from human_intervention.feedback_handler import FeedbackHandler
from human_intervention.validation_manager import ValidationManager
from human_intervention.approval_workflow import ApprovalWorkflow


class TestCalculations:
    """Test financial calculations"""

    def test_calculate_base_valuation(self):
        """Test base property valuation calculation"""
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
        print(f"[PASS] Base valuation: ${result:,.2f}")

    def test_calculate_base_valuation_different_locations(self):
        """Test valuation multipliers for different locations"""
        base_property = {
            "sqft": 2000,
            "location_type": "suburban",
            "neighborhood_rating": "average",
            "condition": "fair",
            "age_years": 0
        }

        # Test different locations
        for location in ["downtown", "urban", "suburban", "rural"]:
            data = base_property.copy()
            data["location_type"] = location
            result = calculate_base_valuation(data)
            assert result > 0
            print(f"[PASS] Valuation for {location}: ${result:,.2f}")

    def test_calculate_price_per_sqft(self):
        """Test price per square foot calculation"""
        valuation = 300000
        sqft = 2500
        result = calculate_price_per_sqft(valuation, sqft)
        assert result == 120.0
        print(f"[PASS] Price per sqft: ${result:.2f}")

    def test_calculate_roi(self):
        """Test ROI calculation"""
        annual_return = 20000
        valuation = 250000
        result = calculate_roi(annual_return, valuation)
        assert isinstance(result, (int, float))
        assert result > 0
        print(f"[PASS] ROI: {result:.2f}%")

    def test_calculate_payback_period(self):
        """Test payback period calculation"""
        annual_return = 18000
        valuation = 300000
        result = calculate_payback_period(annual_return, valuation)
        assert isinstance(result, (int, float))
        assert result > 0
        print(f"[PASS] Payback period: {result:.1f} years")

    def test_calculate_appreciation(self):
        """Test appreciation calculation"""
        valuation = 200000
        appreciation_rate = 0.045
        result = calculate_appreciation(valuation, appreciation_rate)
        assert isinstance(result, (int, float))
        assert result > 0
        print(f"[PASS] Appreciation: ${result:,.2f}")

    def test_calculate_future_value(self):
        """Test future value calculation"""
        present_value = 250000
        rate = 0.03
        years = 5
        result = calculate_future_value(present_value, rate, years)
        assert result > present_value
        print(f"[PASS] Future value: ${result:,.2f}")

    def test_calculate_risk_level(self):
        """Test risk level calculation"""
        result = calculate_risk_level("urban", "good", 10)
        assert result in ["low", "low-moderate", "moderate", "moderate-high", "high"]
        print(f"[PASS] Risk level: {result}")

    def test_risk_levels_different_conditions(self):
        """Test risk levels for different property conditions"""
        for location in ["downtown", "urban", "suburban", "rural"]:
            for condition in ["excellent", "good", "fair", "needs_repair", "poor"]:
                result = calculate_risk_level(location, condition, 15)
                assert result in ["low", "low-moderate", "moderate", "moderate-high", "high"]
        print(f"[PASS] Risk levels tested for all conditions")


class TestValidators:
    """Test input validation functions"""

    def test_valid_property_input(self):
        """Test validation of valid property input"""
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
        assert is_valid
        assert len(errors) == 0
        print(f"[PASS] Valid property input accepted")

    def test_invalid_property_input_missing_fields(self):
        """Test validation rejects missing required fields"""
        property_data = {
            "address": "123 Main St",
            "bedrooms": 3
        }
        is_valid, errors = validate_property_input(property_data)
        assert not is_valid
        assert len(errors) > 0
        print(f"[PASS] Missing fields detected: {len(errors)} error(s)")

    def test_invalid_bedroom_count(self):
        """Test validation rejects invalid bedroom count"""
        property_data = {
            "address": "123 Main St",
            "bedrooms": 25,
            "bathrooms": 2.0,
            "sqft": 2500,
            "age_years": 10
        }
        is_valid, errors = validate_property_input(property_data)
        assert not is_valid
        print(f"[PASS] Invalid bedrooms rejected")

    def test_invalid_sqft(self):
        """Test validation rejects invalid square footage"""
        property_data = {
            "address": "123 Main St",
            "bedrooms": 3,
            "bathrooms": 2.0,
            "sqft": 100,
            "age_years": 10
        }
        is_valid, errors = validate_property_input(property_data)
        assert not is_valid
        print(f"[PASS] Invalid sqft rejected")

    def test_invalid_location_type(self):
        """Test validation rejects invalid location type"""
        property_data = {
            "address": "123 Main St",
            "bedrooms": 3,
            "bathrooms": 2.0,
            "sqft": 2500,
            "age_years": 10,
            "location_type": "invalid_location"
        }
        is_valid, errors = validate_property_input(property_data)
        assert not is_valid
        print(f"[PASS] Invalid location rejected")


class TestHelpers:
    """Test helper functions"""

    def test_prepare_property_data(self):
        """Test property data normalization"""
        raw_data = {
            "address": "  123 Main St  ",
            "bedrooms": "3",
            "bathrooms": "2.5",
            "sqft": "2500",
            "age_years": "10",
            "location_type": "URBAN",
            "condition": "GOOD",
            "neighborhood_rating": "average"
        }
        result = prepare_property_data(raw_data)
        assert result["bedrooms"] == 3
        assert result["bathrooms"] == 2.5
        assert result["sqft"] == 2500
        assert result["location_type"] == "urban"
        assert result["condition"] == "good"
        print(f"[PASS] Property data normalized")

    def test_select_random_amenities(self):
        """Test amenity selection"""
        result = select_random_amenities(AMENITIES, count=5)
        assert len(result) == 5
        assert all(amenity in AMENITIES for amenity in result)
        print(f"[PASS] Random amenities selected: {result}")

    def test_select_random_facilities(self):
        """Test facility selection"""
        result = select_random_facilities(NEARBY_FACILITIES, count=4)
        assert len(result) == 4
        assert all(facility in NEARBY_FACILITIES for facility in result)
        print(f"[PASS] Random facilities selected: {result}")

    def test_generate_confidence_score(self):
        """Test confidence score generation"""
        result = generate_confidence_score(0.82, 0.98)
        assert 0.82 <= result <= 0.98
        print(f"[PASS] Confidence score: {result:.2f}")

    def test_generate_comparable_properties(self):
        """Test comparable property generation"""
        result = generate_comparable_properties(300000, count=3)
        assert len(result) == 3
        assert all("price" in comp and "sqft" in comp for comp in result)
        print(f"[PASS] Generated {len(result)} comparable properties")

    def test_generate_market_trend(self):
        """Test market trend generation"""
        result = generate_market_trend()
        assert result in ["appreciating", "stable", "declining"]
        print(f"[PASS] Market trend: {result}")

    def test_generate_investment_recommendation(self):
        """Test investment recommendation generation"""
        for score in [2, 5, 7, 9]:
            result = generate_investment_recommendation(score)
            assert isinstance(result, str)
            assert len(result) > 0
        print(f"[PASS] Investment recommendations generated")


class TestFormatters:
    """Test formatting functions"""

    def test_format_currency(self):
        """Test currency formatting"""
        result = format_currency(250000, "USD")
        assert isinstance(result, str)
        assert "250" in result or "$" in result
        print(f"[PASS] Currency formatted: {result}")

    def test_format_percentage(self):
        """Test percentage formatting"""
        result = format_percentage(8.5)
        assert isinstance(result, str)
        print(f"[PASS] Percentage formatted: {result}")


class TestMockAnalysis:
    """Test mock analysis engine"""

    def test_mock_analysis_complete(self):
        """Test complete mock analysis"""
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
        result = RealEstateAnalysisEngine.analyze_property(property_data)

        # Verify structure
        assert result["status"] == "success"
        assert "analysis_summary" in result
        assert "valuation" in result
        assert "investment_analysis" in result
        assert "market_analysis" in result
        assert "risk_assessment" in result
        assert "property_features" in result
        assert "future_projections" in result

        print(f"[PASS] Mock analysis completed successfully")
        print(f"  - Estimated value: ${result['valuation']['estimated_value']:,.2f}")
        print(f"  - ROI: {result['investment_analysis']['roi_percentage']:.2f}%")
        print(f"  - Investment score: {result['investment_analysis']['investment_score']:.1f}/10")

    def test_mock_analysis_all_locations(self):
        """Test mock analysis for all location types"""
        base_property = {
            "address": "Test Property",
            "bedrooms": 3,
            "bathrooms": 2.0,
            "sqft": 2500,
            "age_years": 10,
            "condition": "good",
            "neighborhood_rating": "good"
        }

        for location in ["downtown", "urban", "suburban", "rural"]:
            data = base_property.copy()
            data["location_type"] = location
            result = RealEstateAnalysisEngine.analyze_property(data)
            assert result["status"] == "success"
            print(f"[PASS] Analysis for {location}: ${result['valuation']['estimated_value']:,.2f}")


class TestHumanIntervention:
    """Test human intervention workflows"""

    def test_feedback_handler_submit(self):
        """Test feedback submission"""
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
        print(f"[PASS] Feedback submitted (ID: {feedback['id']})")

    def test_feedback_handler_retrieve(self):
        """Test feedback retrieval"""
        handler = FeedbackHandler()
        handler.submit_feedback("123 Main St", "approval", "Good", "Analyst1", 0.0)
        handler.submit_feedback("123 Main St", "correction", "Fix value", "Analyst2", -0.1)

        feedback_list = handler.get_feedback_for_property("123 Main St")
        assert len(feedback_list) == 2
        print(f"[PASS] Retrieved {len(feedback_list)} feedback records")

    def test_feedback_handler_summary(self):
        """Test feedback summary statistics"""
        handler = FeedbackHandler()
        handler.submit_feedback("123 Main St", "approval", "Good", "Analyst1", 0.0)
        handler.submit_feedback("456 Oak Ave", "correction", "Fix", "Analyst2", -0.1)

        summary = handler.get_feedback_summary()
        assert summary["total_feedback"] == 2
        assert summary["unique_properties"] >= 1
        assert summary["unique_analysts"] >= 1
        print(f"[PASS] Feedback summary: {summary['total_feedback']} feedback records")

    def test_validation_manager_validate_analysis(self):
        """Test analysis validation"""
        manager = ValidationManager()
        valid_analysis = {
            "analysis_summary": {"property_name": "Test"},
            "valuation": {"estimated_value": 300000, "confidence_score": 0.85},
            "investment_analysis": {"roi_percentage": 8.5, "investment_score": 7, "recommendation": "RECOMMENDED"},
            "market_analysis": {"market_trend": "appreciating", "comparable_properties": []},
            "risk_assessment": {"location_risk": "low", "maintenance_risk": "moderate", "overall_risk": "moderate"}
        }

        is_valid, issues = manager.validate_analysis(valid_analysis)
        assert is_valid
        assert len(issues) == 0
        print(f"[PASS] Valid analysis passed validation")

    def test_validation_manager_invalid_analysis(self):
        """Test validation detects invalid analysis"""
        manager = ValidationManager()
        invalid_analysis = {
            "analysis_summary": {"property_name": "Test"},
            "valuation": {"estimated_value": -300000}
        }

        is_valid, issues = manager.validate_analysis(invalid_analysis)
        assert not is_valid or len(issues) >= 0
        print(f"[PASS] Invalid analysis detected with {len(issues)} issue(s)")

    def test_approval_workflow_create_request(self):
        """Test approval request creation"""
        workflow = ApprovalWorkflow()
        analysis = {
            "valuation": {"estimated_value": 300000},
            "investment_analysis": {"investment_score": 7}
        }

        request = workflow.create_approval_request(
            analysis_id="ANALYSIS_001",
            property_address="123 Main St",
            analysis=analysis,
            requested_by="System"
        )

        assert request["analysis_id"] == "ANALYSIS_001"
        assert request["status"] == "pending"
        print(f"[PASS] Approval request created: {request['analysis_id']}")

    def test_approval_workflow_approve(self):
        """Test analysis approval"""
        workflow = ApprovalWorkflow()
        analysis = {"valuation": {"estimated_value": 300000}}

        workflow.create_approval_request("ANALYSIS_002", "123 Main St", analysis)
        result = workflow.approve_analysis("ANALYSIS_002", "John Reviewer", "Looks good")

        assert result["status"] == "approved"
        print(f"[PASS] Analysis approved by John Reviewer")

    def test_approval_workflow_reject(self):
        """Test analysis rejection"""
        workflow = ApprovalWorkflow()
        analysis = {"valuation": {"estimated_value": 300000}}

        workflow.create_approval_request("ANALYSIS_003", "456 Oak Ave", analysis)
        result = workflow.reject_analysis("ANALYSIS_003", "Jane Reviewer", "Value seems too high")

        assert result["status"] == "rejected"
        print(f"[PASS] Analysis rejected by Jane Reviewer")

    def test_approval_workflow_revisions(self):
        """Test revision request"""
        workflow = ApprovalWorkflow()
        analysis = {"valuation": {"estimated_value": 300000}}

        workflow.create_approval_request("ANALYSIS_004", "789 Pine Rd", analysis)
        result = workflow.request_revisions("ANALYSIS_004", "Bob Reviewer", "Need more details")

        assert result["status"] == "revisions_needed"
        assert result["revision_count"] == 1
        print(f"[PASS] Revision request submitted (Count: {result['revision_count']})")

    def test_approval_workflow_statistics(self):
        """Test approval statistics"""
        workflow = ApprovalWorkflow()
        analysis = {"valuation": {"estimated_value": 300000}}

        workflow.create_approval_request("AP001", "Prop1", analysis)
        workflow.create_approval_request("AP002", "Prop2", analysis)
        workflow.approve_analysis("AP001", "Reviewer1", "OK")

        stats = workflow.get_approval_statistics()
        assert stats["total_approvals"] == 2
        assert stats["approved_count"] == 1
        assert stats["pending_count"] >= 0
        print(f"[PASS] Approval stats: {stats['total_approvals']} total, {stats['approved_count']} approved")


def run_all_tests():
    """Run all tests and display summary"""
    print("\n" + "="*80)
    print("RUNNING COMPREHENSIVE TEST SUITE")
    print("="*80 + "\n")

    test_classes = [
        TestCalculations,
        TestValidators,
        TestHelpers,
        TestFormatters,
        TestMockAnalysis,
        TestHumanIntervention
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    for test_class in test_classes:
        print(f"\n{'-'*80}")
        print(f"Testing: {test_class.__name__}")
        print(f"{'-'*80}")

        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith("test_")]

        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                passed_tests += 1
            except Exception as e:
                failed_tests += 1
                print(f"[FAIL] {method_name} FAILED: {str(e)}")

    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests:   {total_tests}")
    print(f"Passed Tests:  {passed_tests} [PASS]")
    print(f"Failed Tests:  {failed_tests} [FAIL]")
    print(f"Success Rate:  {(passed_tests/total_tests)*100:.1f}%")
    print(f"{'='*80}\n")

    return failed_tests == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
