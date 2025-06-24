# utils/financial_calculations.py
"""
This module contains general-purpose financial calculation functions
that can be reused across different financial instruments and strategies.
"""
import numpy as np

def calculate_log_returns(prices: np.ndarray) -> np.ndarray:
    """
    Calculates the log returns of a price series.

    Args:
        prices (np.ndarray): An array of prices.

    Returns:
        np.ndarray: An array of log returns.
    """
    if prices.ndim != 1 or len(prices) < 2:
        raise ValueError("Price series must be a 1D array with at least two values.")

    # Log returns are calculated as ln(P_t / P_{t-1})
    log_returns = np.log(prices[1:] / prices[:-1])
    return log_returns

# Other general calculations like CAGR, TVM functions, etc. could be added here.