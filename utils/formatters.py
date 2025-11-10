"""
Formatting utilities for Real Estate Intelligence System
Handles currency, percentages, dates, and other data formatting
"""

from datetime import datetime
from typing import Union, Optional


def format_currency(amount: Union[int, float], currency: str = "USD", decimal_places: int = 2) -> str:
    """
    Format amount as currency string

    Args:
        amount: Numeric amount to format
        currency: Currency code (USD, EUR, GBP, etc.)
        decimal_places: Number of decimal places

    Returns:
        Formatted currency string
    """
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹",
        "JPY": "¥"
    }

    symbol = currency_symbols.get(currency, currency)

    if amount >= 1_000_000:
        return f"{symbol}{amount / 1_000_000:,.{decimal_places}f}M"
    elif amount >= 1_000:
        return f"{symbol}{amount / 1_000:,.{decimal_places}f}K"
    else:
        return f"{symbol}{amount:,.{decimal_places}f}"


def format_percentage(value: Union[int, float], decimal_places: int = 2) -> str:
    """
    Format value as percentage string

    Args:
        value: Numeric value to format (0.95 for 95%)
        decimal_places: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimal_places}f}%"


def format_date(date_obj: Optional[datetime] = None, date_format: str = "%Y-%m-%d") -> str:
    """
    Format datetime object as string

    Args:
        date_obj: Datetime object to format (None for current time)
        date_format: Format string

    Returns:
        Formatted date string
    """
    if date_obj is None:
        date_obj = datetime.now()

    return date_obj.strftime(date_format)


def format_address(address: str) -> str:
    """
    Format address string with proper capitalization

    Args:
        address: Address string

    Returns:
        Formatted address
    """
    return " ".join(word.capitalize() for word in address.split())


def format_number(number: Union[int, float], decimal_places: int = 2) -> str:
    """
    Format number with thousands separator

    Args:
        number: Number to format
        decimal_places: Number of decimal places

    Returns:
        Formatted number string
    """
    return f"{number:,.{decimal_places}f}"


def format_duration(days: int) -> str:
    """
    Format duration in days to human readable format

    Args:
        days: Number of days

    Returns:
        Formatted duration string
    """
    years = days // 365
    remaining_days = days % 365
    months = remaining_days // 30

    if years > 0 and months > 0:
        return f"{years} year(s) {months} month(s)"
    elif years > 0:
        return f"{years} year(s)"
    elif months > 0:
        return f"{months} month(s)"
    else:
        return f"{days} day(s)"
