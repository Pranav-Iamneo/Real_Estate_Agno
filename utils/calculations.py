"""
Calculation utilities for Real Estate Intelligence System
Handles valuation, ROI, appreciation, and financial calculations
"""

from typing import Dict, Any
import math


# Market data constants
LOCATION_MULTIPLIERS = {
    "downtown": 1.4,
    "urban": 1.2,
    "suburban": 1.0,
    "rural": 0.7
}

NEIGHBORHOOD_FACTORS = {
    "excellent": 1.3,
    "good": 1.1,
    "average": 1.0,
    "developing": 0.85,
    "poor": 0.6
}

CONDITION_FACTORS = {
    "excellent": 1.2,
    "good": 1.1,
    "fair": 1.0,
    "needs_repair": 0.75,
    "poor": 0.5
}


def calculate_base_valuation(property_data: Dict[str, Any]) -> float:
    """
    Calculate base property valuation based on property characteristics

    Args:
        property_data: Dictionary with property details

    Returns:
        Estimated property valuation in USD
    """
    # Base price per sqft
    base_price_per_sqft = 150

    # Get property attributes
    sqft = property_data.get("sqft", 2000)
    location = property_data.get("location_type", "suburban").lower()
    neighborhood = property_data.get("neighborhood_rating", "average").lower()
    condition = property_data.get("condition", "fair").lower()
    age_years = property_data.get("age_years", 0)

    # Get multipliers with defaults
    location_multiplier = LOCATION_MULTIPLIERS.get(location, 1.0)
    neighborhood_multiplier = NEIGHBORHOOD_FACTORS.get(neighborhood, 1.0)
    condition_multiplier = CONDITION_FACTORS.get(condition, 1.0)

    # Calculate age depreciation (2% per year, minimum 50%)
    age_factor = max(0.5, 1.0 - (age_years * 0.02))

    # Calculate final valuation
    valuation = sqft * base_price_per_sqft * location_multiplier * \
                neighborhood_multiplier * condition_multiplier * age_factor

    return round(valuation, 2)


def calculate_price_per_sqft(valuation: float, sqft: int) -> float:
    """
    Calculate price per square foot

    Args:
        valuation: Total property valuation
        sqft: Property square footage

    Returns:
        Price per square foot
    """
    if sqft <= 0:
        return 0
    return round(valuation / sqft, 2)


def calculate_roi(annual_return: float, valuation: float) -> float:
    """
    Calculate return on investment percentage

    Args:
        annual_return: Annual return amount
        valuation: Total property valuation

    Returns:
        ROI percentage
    """
    if valuation <= 0:
        return 0
    return round((annual_return / valuation) * 100, 2)


def calculate_payback_period(valuation: float, annual_return: float) -> float:
    """
    Calculate payback period in years

    Args:
        valuation: Total property valuation
        annual_return: Annual return amount

    Returns:
        Payback period in years
    """
    if annual_return <= 0:
        return float('inf')
    return round(valuation / annual_return, 2)


def calculate_appreciation(valuation: float, appreciation_rate: float = 0.045) -> float:
    """
    Calculate annual property appreciation

    Args:
        valuation: Current property valuation
        appreciation_rate: Annual appreciation rate (default 4.5%)

    Returns:
        Annual appreciation amount
    """
    return round(valuation * appreciation_rate, 2)


def calculate_rental_income(valuation: float, rental_yield: float = 0.065) -> float:
    """
    Calculate annual rental income potential

    Args:
        valuation: Current property valuation
        rental_yield: Annual rental yield (default 6.5%)

    Returns:
        Annual rental income
    """
    return round(valuation * rental_yield, 2)


def calculate_total_annual_return(rental_income: float, appreciation: float) -> float:
    """
    Calculate total annual return

    Args:
        rental_income: Annual rental income
        appreciation: Annual appreciation

    Returns:
        Total annual return
    """
    return round(rental_income + appreciation, 2)


def calculate_future_value(present_value: float, annual_rate: float, years: int) -> float:
    """
    Calculate future value using compound growth

    Args:
        present_value: Current value
        annual_rate: Annual growth rate (0.045 for 4.5%)
        years: Number of years

    Returns:
        Projected future value
    """
    if years <= 0 or annual_rate < 0:
        return present_value

    future_value = present_value * ((1 + annual_rate) ** years)
    return round(future_value, 2)


def calculate_cumulative_return(annual_amount: float, years: int) -> float:
    """
    Calculate cumulative return over multiple years

    Args:
        annual_amount: Annual return/income
        years: Number of years

    Returns:
        Cumulative total
    """
    return round(annual_amount * years, 2)


def calculate_investment_score(roi: float, valuation: float,
                               condition_rating: float = 0.5) -> int:
    """
    Calculate investment score from 1-10

    Args:
        roi: ROI percentage
        valuation: Property valuation
        condition_rating: Condition factor (0-1)

    Returns:
        Investment score (1-10)
    """
    # ROI scoring (0-4 points)
    roi_score = min(4, roi / 2.5)

    # Valuation scoring (0-3 points)
    # Properties between $200k-$600k get better scores
    if 200_000 <= valuation <= 600_000:
        valuation_score = 3
    elif 100_000 <= valuation < 1_000_000:
        valuation_score = 2.5
    else:
        valuation_score = 2

    # Condition scoring (0-3 points)
    condition_score = condition_rating * 3

    total_score = roi_score + valuation_score + condition_score
    return int(min(10, max(1, round(total_score))))


def calculate_risk_level(location_type: str, condition: str, age_years: int) -> str:
    """
    Calculate overall risk level based on property characteristics

    Args:
        location_type: Type of location
        condition: Property condition
        age_years: Age of property in years

    Returns:
        Risk level: low, low-moderate, moderate, moderate-high, high
    """
    risk_score = 0

    # Location risk
    location_risk_map = {
        "downtown": 2,
        "urban": 2,
        "suburban": 3,
        "rural": 4
    }
    risk_score += location_risk_map.get(location_type.lower(), 3)

    # Condition risk
    condition_risk_map = {
        "excellent": 1,
        "good": 2,
        "fair": 3,
        "needs_repair": 4,
        "poor": 5
    }
    risk_score += condition_risk_map.get(condition.lower(), 3)

    # Age risk (properties over 50 years add risk)
    if age_years > 50:
        risk_score += 3
    elif age_years > 30:
        risk_score += 2
    elif age_years > 50:
        risk_score += 1

    # Normalize and classify
    avg_risk = risk_score / 3

    if avg_risk < 1.5:
        return "low"
    elif avg_risk < 2.5:
        return "low-moderate"
    elif avg_risk < 3.5:
        return "moderate"
    elif avg_risk < 4.5:
        return "moderate-high"
    else:
        return "high"
