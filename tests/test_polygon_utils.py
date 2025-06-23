# tests/test_polygon_utils.py

import pytest
import datetime
from utils.polygon_utils import (
    format_polygon_option_symbol,
    format_polygon_ticker,
    to_polygon_date_str,
    to_polygon_nanosecond_timestamp
)

# --- Tests for format_polygon_option_symbol ---

def test_format_option_symbol_standard_call():
    """Tests standard formatting for a call option."""
    symbol = format_polygon_option_symbol("AAPL", "250117", "C", 170.0)
    assert symbol == "O:AAPL250117C00170000"

def test_format_option_symbol_fractional_strike_put():
    """Tests formatting for a put option with a fractional strike price."""
    symbol = format_polygon_option_symbol("SPY", "250620", "P", 450.50)
    assert symbol == "O:SPY250620P00450500"

def test_format_option_symbol_invalid_date():
    """Tests that the function raises a ValueError for an invalid date string."""
    with pytest.raises(ValueError, match="must be 6 digits"):
        format_polygon_option_symbol("TSLA", "25011", "C", 180.0)

def test_format_option_symbol_invalid_type():
    """Tests that the function raises a ValueError for an invalid option type."""
    with pytest.raises(ValueError, match="must be 'C' or 'P'"):
        format_polygon_option_symbol("MSFT", "250321", "X", 300.0)

def test_format_option_symbol_negative_strike():
    """Tests that the function raises a ValueError for a negative strike price."""
    with pytest.raises(ValueError, match="must be a positive number"):
        format_polygon_option_symbol("GOOG", "251219", "C", -150.0)


# --- Tests for format_polygon_ticker ---

def test_format_polygon_ticker_stock():
    """Tests formatting for a standard stock ticker."""
    assert format_polygon_ticker("AAPL", asset_class='stocks') == "AAPL"
    assert format_polygon_ticker("aapl") == "AAPL"  # Test case insensitivity and default

def test_format_polygon_ticker_index():
    """Tests formatting for an index ticker."""
    assert format_polygon_ticker("SPX", asset_class='indices') == "I:SPX"

def test_format_polygon_ticker_crypto():
    """Tests formatting for a crypto ticker."""
    assert format_polygon_ticker("BTC-USD", asset_class='crypto') == "X:BTC-USD"
    
def test_format_polygon_ticker_invalid_class():
    """Tests that the function raises an error for an invalid asset class."""
    with pytest.raises(ValueError, match="Invalid asset class"):
        format_polygon_ticker("TEST", asset_class='futures')


# --- Tests for date/timestamp formatters ---

def test_to_polygon_date_str():
    """Tests the conversion of a datetime object to a YYYY-MM-DD string."""
    dt = datetime.date(2025, 6, 22)
    assert to_polygon_date_str(dt) == "2025-06-22"

def test_to_polygon_nanosecond_timestamp():
    """Tests the conversion of a datetime object to a nanosecond timestamp."""
    # Using a known timestamp for a specific UTC datetime
    dt = datetime.datetime(2025, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    expected_ts = 1735689600 * 1_000_000_000
    assert to_polygon_nanosecond_timestamp(dt) == expected_ts