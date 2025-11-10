"""
Helper utilities for Real Estate Intelligence System
Common functions for data processing and response handling
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
import json


def prepare_property_data(property_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare and normalize property input data

    Args:
        property_input: Raw property input data

    Returns:
        Normalized property data dictionary
    """
    return {
        "address": property_input.get("address", "").strip(),
        "bedrooms": int(property_input.get("bedrooms", 1)),
        "bathrooms": float(property_input.get("bathrooms", 1.0)),
        "sqft": int(property_input.get("sqft", 2000)),
        "age_years": int(property_input.get("age_years", 0)),
        "location_type": property_input.get("location_type", "suburban").lower(),
        "condition": property_input.get("condition", "fair").lower(),
        "neighborhood_rating": property_input.get("neighborhood_rating", "average").lower()
    }


def select_random_amenities(amenities_list: List[str], count: int = 5) -> List[str]:
    """
    Select random amenities from list

    Args:
        amenities_list: Full list of available amenities
        count: Number of amenities to select

    Returns:
        List of selected amenities
    """
    if not amenities_list:
        return []

    count = min(count, len(amenities_list))
    return random.sample(amenities_list, count)


def select_random_facilities(facilities_list: List[str], count: int = 4) -> List[str]:
    """
    Select random nearby facilities from list

    Args:
        facilities_list: Full list of available facilities
        count: Number of facilities to select

    Returns:
        List of selected facilities
    """
    if not facilities_list:
        return []

    count = min(count, len(facilities_list))
    return random.sample(facilities_list, count)


def generate_confidence_score(min_score: float = 0.82, max_score: float = 0.98) -> float:
    """
    Generate random confidence score for valuation

    Args:
        min_score: Minimum confidence score
        max_score: Maximum confidence score

    Returns:
        Random confidence score between min and max
    """
    return round(random.uniform(min_score, max_score), 2)


def generate_comparable_properties(base_price: float, count: int = 3) -> List[Dict[str, Any]]:
    """
    Generate comparable property data for market analysis

    Args:
        base_price: Base property price for comparables
        count: Number of comparables to generate

    Returns:
        List of comparable property dictionaries
    """
    comparables = []

    for i in range(count):
        # Generate price within 10% of base price
        price_variation = random.uniform(0.9, 1.1)
        comp_price = round(base_price * price_variation, 2)

        # Generate comparable data
        base_sqft = int(base_price / 150)
        comp = {
            "address": f"Nearby Property {i + 1}",
            "price": comp_price,
            "sqft": random.randint(int(base_sqft * 0.9), int(base_sqft * 1.1)),
            "beds": random.randint(2, 5),
            "price_per_sqft": round(comp_price / random.randint(2000, 3000), 2)
        }
        comparables.append(comp)

    return comparables


def generate_market_trend() -> str:
    """
    Generate random market trend

    Returns:
        Market trend (appreciating, stable, declining)
    """
    trends = ["appreciating", "stable", "declining"]
    return random.choice(trends)


def generate_market_growth_rate() -> str:
    """
    Generate random market growth rate

    Returns:
        Market growth rate as string (e.g., "3.8% annually")
    """
    rate = round(random.uniform(1.5, 6.5), 1)
    return f"{rate}% annually"


def generate_investment_recommendation(score: int) -> str:
    """
    Generate investment recommendation based on score

    Args:
        score: Investment score (1-10)

    Returns:
        Recommendation string
    """
    if score >= 8:
        return "STRONG_BUY - Excellent investment opportunity"
    elif score >= 6:
        return "RECOMMENDED - Good investment with solid returns"
    elif score >= 4:
        return "NEUTRAL - Consider carefully before investing"
    else:
        return "NOT_RECOMMENDED - High risk relative to returns"


def generate_strengths(condition: str, location: str, bedrooms: int) -> List[str]:
    """
    Generate property strengths based on characteristics

    Args:
        condition: Property condition
        location: Location type
        bedrooms: Number of bedrooms

    Returns:
        List of property strengths
    """
    strengths = []

    if condition in ["excellent", "good"]:
        strengths.append("Well-maintained property requiring minimal repairs")

    if location in ["downtown", "urban"]:
        strengths.append("Prime location with high walkability")

    if bedrooms >= 3:
        strengths.append("Spacious layout ideal for families")

    strengths.append("Excellent amenities and facilities")

    return strengths


def generate_weaknesses(condition: str, age_years: int) -> List[str]:
    """
    Generate property weaknesses based on characteristics

    Args:
        condition: Property condition
        age_years: Property age in years

    Returns:
        List of property weaknesses
    """
    weaknesses = []

    if condition in ["needs_repair", "poor"]:
        weaknesses.append("Property requires significant maintenance or repairs")

    if age_years > 50:
        weaknesses.append("Older property with potential structural concerns")

    if not weaknesses:
        weaknesses.append("Monitor market trends")

    return weaknesses


def create_api_response(status: str, data: Optional[Dict[str, Any]] = None,
                       message: Optional[str] = None,
                       timestamp: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Create standardized API response

    Args:
        status: Response status (success, error, pending)
        data: Response data
        message: Optional message
        timestamp: Response timestamp

    Returns:
        Formatted API response dictionary
    """
    if timestamp is None:
        timestamp = datetime.now()

    response = {
        "status": status,
        "timestamp": timestamp.isoformat()
    }

    if data:
        response["data"] = data

    if message:
        response["message"] = message

    return response


def merge_analysis_results(mock_analysis: Dict[str, Any],
                          agent_enhancements: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge mock analysis with agent enhancements

    Args:
        mock_analysis: Base mock analysis data
        agent_enhancements: List of agent enhancement dictionaries

    Returns:
        Merged analysis dictionary
    """
    merged = mock_analysis.copy()

    for enhancement in agent_enhancements:
        if not enhancement:
            continue

        # Merge top-level keys
        for key, value in enhancement.items():
            if key not in merged:
                merged[key] = value
            elif isinstance(value, dict) and isinstance(merged.get(key), dict):
                # Deep merge dictionaries
                merged[key].update(value)

    return merged


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length with ellipsis

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def safe_get_nested(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """
    Safely get nested dictionary value

    Args:
        data: Dictionary to search
        keys: List of keys to traverse
        default: Default value if not found

    Returns:
        Value at nested key or default
    """
    current = data
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return default

    return current if current is not None else default


def safe_set_nested(data: Dict[str, Any], keys: List[str], value: Any) -> Dict[str, Any]:
    """
    Safely set nested dictionary value, creating intermediate dicts as needed

    Args:
        data: Dictionary to modify
        keys: List of keys to traverse
        value: Value to set

    Returns:
        Modified dictionary
    """
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value
    return data
