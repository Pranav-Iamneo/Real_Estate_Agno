"""
Constants and configuration values for Real Estate Intelligence System
"""

# Market data
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

# Property characteristics
VALID_LOCATION_TYPES = ["downtown", "urban", "suburban", "rural"]
VALID_CONDITIONS = ["excellent", "good", "fair", "needs_repair", "poor"]
VALID_NEIGHBORHOOD_RATINGS = ["excellent", "good", "average", "developing", "poor"]

# Financial calculations
BASE_PRICE_PER_SQFT = 150
AGE_DEPRECIATION_RATE = 0.02  # 2% per year
MINIMUM_AGE_FACTOR = 0.5  # 50% minimum value retention

DEFAULT_APPRECIATION_RATE = 0.045  # 4.5% annual
DEFAULT_RENTAL_YIELD = 0.065  # 6.5% annual
APPRECIATION_RANGE = (0.03, 0.06)  # 3-6% range
RENTAL_YIELD_RANGE = (0.05, 0.08)  # 5-8% range

# Property value ranges
MIN_PROPERTY_VALUE = 50_000
MAX_PROPERTY_VALUE = 10_000_000
MIN_SQFT = 500
MAX_SQFT = 1_000_000
MIN_BEDROOMS = 1
MAX_BEDROOMS = 20
MIN_BATHROOMS = 0.5
MAX_BATHROOMS = 20
MIN_AGE = 0
MAX_AGE = 200

# Confidence scores
MIN_CONFIDENCE = 0.70  # 70%
MAX_CONFIDENCE = 0.98  # 98%

# Investment scoring
INVESTMENT_SCORE_RANGE = (1, 10)
INVESTMENT_CATEGORIES = {
    "high": (8, 10),
    "moderate": (6, 7),
    "low": (4, 5),
    "very_low": (1, 3)
}

# Risk levels
RISK_LEVELS = ["low", "low-moderate", "moderate", "moderate-high", "high"]

# Amenities list
AMENITIES = [
    "Swimming Pool",
    "Gym",
    "Parking",
    "Garden",
    "Balcony",
    "Security System",
    "AC",
    "Water Tank",
    "Solar Panels",
    "Home Theater",
    "Elevator",
    "CCTV",
    "Power Backup",
    "Guest House",
    "Garage"
]

# Nearby facilities
NEARBY_FACILITIES = [
    "Schools",
    "Hospital",
    "Shopping Mall",
    "Metro Station",
    "Parks",
    "Restaurants",
    "Banks",
    "Libraries",
    "Police Station",
    "Fire Station",
    "Universities",
    "Government Offices"
]

# Market trends
MARKET_TRENDS = ["appreciating", "stable", "declining"]
MARKET_TREND_DESCRIPTIONS = {
    "appreciating": "Property values are increasing",
    "stable": "Property values are stable",
    "declining": "Property values are decreasing"
}

# Location desirability ratings
LOCATION_DESIRABILITY_RATINGS = ["excellent", "very_good", "good", "average", "poor"]

# ROI categories
ROI_CATEGORIES = {
    "excellent": (12, 100),
    "very_good": (9, 12),
    "good": (6, 9),
    "moderate": (3, 6),
    "low": (0, 3)
}

# Recommendation types
RECOMMENDATION_TYPES = [
    "STRONG_BUY",
    "RECOMMENDED",
    "NEUTRAL",
    "NOT_RECOMMENDED"
]

# Time periods
PROJECTION_YEARS = 5
HOLDING_PERIOD_YEARS = 10

# Currency symbols
CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "INR": "₹",
    "JPY": "¥",
    "CAD": "C$",
    "AUD": "A$"
}

# API response status codes
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_PENDING = "pending"
STATUS_FAILED = "failed"

# Logging
DEFAULT_LOG_LEVEL = "INFO"
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Default values
DEFAULT_LOCATION_TYPE = "suburban"
DEFAULT_CONDITION = "fair"
DEFAULT_NEIGHBORHOOD_RATING = "average"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
