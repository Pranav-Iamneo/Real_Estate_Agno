"""
Validation utilities for Real Estate Intelligence System
Validates property data and configuration parameters
"""

from typing import Dict, Any, Tuple, List


# Valid values for property attributes
VALID_LOCATION_TYPES = ["downtown", "urban", "suburban", "rural"]
VALID_CONDITIONS = ["excellent", "good", "fair", "needs_repair", "poor"]
VALID_NEIGHBORHOOD_RATINGS = ["excellent", "good", "average", "developing", "poor"]


def validate_location_type(location_type: str) -> Tuple[bool, str]:
    """
    Validate location type

    Args:
        location_type: Location type to validate

    Returns:
        Tuple of (is_valid, message)
    """
    location_lower = location_type.lower()
    if location_lower not in VALID_LOCATION_TYPES:
        return False, f"Invalid location type. Must be one of: {', '.join(VALID_LOCATION_TYPES)}"
    return True, "Valid location type"


def validate_condition(condition: str) -> Tuple[bool, str]:
    """
    Validate property condition

    Args:
        condition: Property condition to validate

    Returns:
        Tuple of (is_valid, message)
    """
    condition_lower = condition.lower()
    if condition_lower not in VALID_CONDITIONS:
        return False, f"Invalid condition. Must be one of: {', '.join(VALID_CONDITIONS)}"
    return True, "Valid condition"


def validate_neighborhood_rating(rating: str) -> Tuple[bool, str]:
    """
    Validate neighborhood rating

    Args:
        rating: Neighborhood rating to validate

    Returns:
        Tuple of (is_valid, message)
    """
    rating_lower = rating.lower()
    if rating_lower not in VALID_NEIGHBORHOOD_RATINGS:
        return False, f"Invalid rating. Must be one of: {', '.join(VALID_NEIGHBORHOOD_RATINGS)}"
    return True, "Valid neighborhood rating"


def validate_property_input(property_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate complete property input data

    Args:
        property_data: Dictionary containing property information

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate required fields
    required_fields = ["address", "bedrooms", "bathrooms", "sqft", "age_years",
                       "location_type", "condition", "neighborhood_rating"]

    for field in required_fields:
        if field not in property_data:
            errors.append(f"Missing required field: {field}")

    if errors:
        return False, errors

    # Validate address
    address = property_data.get("address", "").strip()
    if not address or len(address) < 5:
        errors.append("Address must be at least 5 characters long")

    # Validate bedrooms
    try:
        bedrooms = int(property_data.get("bedrooms", 0))
        if bedrooms < 1 or bedrooms > 20:
            errors.append("Bedrooms must be between 1 and 20")
    except (ValueError, TypeError):
        errors.append("Bedrooms must be an integer")

    # Validate bathrooms
    try:
        bathrooms = float(property_data.get("bathrooms", 0))
        if bathrooms < 0.5 or bathrooms > 20:
            errors.append("Bathrooms must be between 0.5 and 20")
    except (ValueError, TypeError):
        errors.append("Bathrooms must be a number")

    # Validate sqft
    try:
        sqft = int(property_data.get("sqft", 0))
        if sqft < 500 or sqft > 1_000_000:
            errors.append("Square footage must be between 500 and 1,000,000")
    except (ValueError, TypeError):
        errors.append("Square footage must be an integer")

    # Validate age_years
    try:
        age_years = int(property_data.get("age_years", 0))
        if age_years < 0 or age_years > 200:
            errors.append("Property age must be between 0 and 200 years")
    except (ValueError, TypeError):
        errors.append("Property age must be an integer")

    # Validate location_type
    location_type = property_data.get("location_type", "")
    is_valid, msg = validate_location_type(location_type)
    if not is_valid:
        errors.append(msg)

    # Validate condition
    condition = property_data.get("condition", "")
    is_valid, msg = validate_condition(condition)
    if not is_valid:
        errors.append(msg)

    # Validate neighborhood_rating
    rating = property_data.get("neighborhood_rating", "")
    is_valid, msg = validate_neighborhood_rating(rating)
    if not is_valid:
        errors.append(msg)

    return len(errors) == 0, errors


def validate_numeric_range(value: float, min_val: float, max_val: float,
                          field_name: str = "Value") -> Tuple[bool, str]:
    """
    Validate numeric value is within range

    Args:
        value: Value to validate
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
        field_name: Name of field for error message

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        num_value = float(value)
        if num_value < min_val or num_value > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}"
        return True, f"{field_name} is valid"
    except (ValueError, TypeError):
        return False, f"{field_name} must be a number"
