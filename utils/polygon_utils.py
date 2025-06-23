# utils/polygon_utils.py
import datetime
from typing import Union

def format_polygon_option_symbol(underlying_ticker: str, expiration_date_str: str, option_type: str, strike_price: float) -> str:
    """
    Formats an option symbol into the standard Polygon.io format.
    Example: underlying_ticker="AAPL", expiration_date_str="250117",
             option_type="C", strike_price=170.0
             returns "O:AAPL250117C00170000"

    Args:
        underlying_ticker (str): The stock ticker (e.g., "AAPL"). Must be non-empty.
        expiration_date_str (str): Expiration date in "YYMMDD" format (e.g., "250117" for Jan 17, 2025).
                                   Must be a 6-digit string.
        option_type (str): 'C' for Call or 'P' for Put. Case-insensitive.
        strike_price (float): The strike price of the option. Must be a positive number.

    Returns:
        str: The formatted Polygon.io option symbol.

    Raises:
        ValueError: If any input parameters are invalid.
    """
    # FIX: Pylance knows this is a string from the type hint, so the isinstance check is removed.
    if not underlying_ticker.strip():
        raise ValueError("Underlying ticker must be a non-empty string.")
    
    # FIX: Redundant isinstance check removed.
    if not (len(expiration_date_str) == 6 and expiration_date_str.isdigit()):
        raise ValueError(f"Expiration date string must be 6 digits (YYMMDD), got: '{expiration_date_str}'")
        
    processed_option_type = option_type.upper()
    if processed_option_type not in ['C', 'P']:
        raise ValueError(f"Option type must be 'C' or 'P', got: '{option_type}'")
    
    # FIX: Redundant isinstance check removed. The type hint already specifies float.
    if strike_price <= 0:
        raise ValueError(f"Strike price must be a positive number, got: {strike_price}")

    strike_as_int_scaled = int(strike_price * 1000)
    strike_formatted = str(strike_as_int_scaled).zfill(8)
    
    return f"O:{underlying_ticker.upper().strip()}{expiration_date_str}{processed_option_type}{strike_formatted}"


def format_polygon_ticker(symbol: str, asset_class: str = 'stocks') -> str:
    """
    Formats a symbol into a Polygon.io-compatible ticker with appropriate prefixes.

    Args:
        symbol (str): The base symbol (e.g., "SPX", "EURUSD", "BTC").
        asset_class (str): The asset class. One of 'stocks', 'indices', 
                           'crypto', or 'forex'. Defaults to 'stocks'.

    Returns:
        str: The formatted ticker string (e.g., "I:SPX").
    """
    prefix_map = {
        'stocks': '',
        'indices': 'I:',
        'crypto': 'X:', # Crypto uses 'X:' prefix
        'forex': 'C:'   # Forex uses 'C:' prefix
    }
    
    # FIX: More direct logic that avoids the impossible "is None" check.
    asset_class_lower = asset_class.lower()
    if asset_class_lower not in prefix_map:
        raise ValueError(f"Invalid asset class '{asset_class}'. Must be one of {list(prefix_map.keys())}")

    prefix = prefix_map[asset_class_lower]
    return f"{prefix}{symbol.upper()}"


def to_polygon_date_str(dt_object: Union[datetime.datetime, datetime.date]) -> str:
    """
    Converts a datetime or date object to the 'YYYY-MM-DD' string format
    required by the Polygon API.

    Args:
        dt_object (Union[datetime.datetime, datetime.date]): The date or datetime object.

    Returns:
        str: The formatted date string.
    """
    return dt_object.strftime('%Y-%m-%d')


def to_polygon_nanosecond_timestamp(dt_object: datetime.datetime) -> int:
    """
    Converts a datetime object to a nanosecond integer timestamp as required
    by some Polygon API endpoints.

    Args:
        dt_object (datetime.datetime): The datetime object to convert.

    Returns:
        int: The timestamp in nanoseconds.
    """
    return int(dt_object.timestamp() * 1e9)