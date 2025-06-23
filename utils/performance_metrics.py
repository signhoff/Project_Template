# utils/performance_metrics.py
"""
This module contains functions for calculating common portfolio and strategy
performance metrics, such as Sharpe Ratio, Sortino Ratio, Max Drawdown, etc.
"""

import logging
import numpy as np
import pandas as pd
from typing import Union, Any

# Inherits the central logging configuration
logger = logging.getLogger(__name__)

# Define a more specific type hint for a series or array of floats
NumericSeriesOrArray = Union[pd.Series[float], np.ndarray[Any, np.dtype[np.float64]]]


def calculate_sharpe_ratio(
    returns: NumericSeriesOrArray,
    risk_free_rate: float,
    periods_per_year: int = 252
) -> float:
    """
    Calculates the annualized Sharpe Ratio of a strategy.

    Args:
        returns (Union[pd.Series[float], np.ndarray]): A pandas Series or NumPy
            array of periodic returns (e.g., daily returns).
        risk_free_rate (float): The annualized risk-free interest rate.
        periods_per_year (int): The number of trading periods in a year.

    Returns:
        float: The annualized Sharpe Ratio.
    """
    periodic_risk_free_rate: float = (1 + risk_free_rate)**(1 / periods_per_year) - 1
    excess_returns: NumericSeriesOrArray = returns - periodic_risk_free_rate
    
    # FIX: Explicitly convert the NumPy float type to a standard Python float.
    std_dev_returns: float = float(np.std(excess_returns))
    
    if std_dev_returns == 0:
        logger.warning("Standard deviation of returns is zero. Cannot calculate Sharpe Ratio. Returning 0.0.")
        return 0.0
        
    # FIX: Explicitly convert the result of the calculation to a standard Python float.
    sharpe_ratio_periodic: float = float(np.mean(excess_returns) / std_dev_returns)
    annualized_sharpe_ratio: float = sharpe_ratio_periodic * np.sqrt(periods_per_year)
    
    return float(annualized_sharpe_ratio)


def calculate_max_drawdown(
    equity_curve: NumericSeriesOrArray
) -> float:
    """
    Calculates the Maximum Drawdown (MDD) from an equity curve.

    Args:
        equity_curve (Union[pd.Series[float], np.ndarray]): A pandas Series or
            NumPy array representing the portfolio's value over time.

    Returns:
        float: The Maximum Drawdown as a negative decimal.
    """
    high_water_mark: NumericSeriesOrArray = np.maximum.accumulate(equity_curve)
    drawdown: NumericSeriesOrArray = (equity_curve - high_water_mark) / high_water_mark
    
    # FIX: Explicitly convert the NumPy float type to a standard Python float.
    max_drawdown: float = float(np.min(drawdown))
    
    return max_drawdown