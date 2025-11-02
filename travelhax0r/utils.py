"""
Utility functions for the TravelHax0r MCP server.
"""

import re


def parse_duration(duration_str: str) -> int:
    """
    Parse duration string like "14 hr 35 min" into total minutes.

    Args:
        duration_str: Duration string from flight data

    Returns:
        Total duration in minutes
    """
    hours = 0
    minutes = 0

    if "hr" in duration_str:
        hours_part = duration_str.split("hr")[0].strip()
        hours = int(hours_part) if hours_part.isdigit() else 0

    if "min" in duration_str:
        min_part = duration_str.split("min")[0].split()[-1]
        minutes = int(min_part) if min_part.isdigit() else 0

    return hours * 60 + minutes


def parse_price(price_str: str) -> float:
    """
    Parse price string into a float value.

    Removes all non-digit and non-dot characters and converts to float.
    Examples: "$601" -> 601.0, "€450.50" -> 450.50

    Args:
        price_str: Price string from flight data

    Returns:
        Price as a float value
    """
    # Remove all characters except digits and dots
    numeric_str = re.sub(r"[^\d.]", "", price_str)
    return float(numeric_str) if numeric_str else 0.0
