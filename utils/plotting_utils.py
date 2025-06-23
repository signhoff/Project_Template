# utils/plotting_utils.py
"""
This file contains generic, reusable functions for creating Matplotlib plots.
These functions return Figure objects and are not tied to any specific GUI framework.
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, Optional

from matplotlib.figure import Figure

def create_pnl_figure(
    strategy_details: Dict[str, Any],
    ticker_symbol: str,
    current_price: float,
    lower_2_sigma_target: Optional[float],
    upper_2_sigma_target: Optional[float],
    currency: str = "$"
) -> Figure: # FIX: Use the directly imported Figure type
    """
    Creates a Matplotlib Figure object for a strategy's P&L curve.

    This function contains only the plotting logic and is decoupled from any
    GUI framework like Tkinter.

    Args:
        strategy_details (Dict[str, Any]): Dictionary with P&L data.
        ticker_symbol (str): The stock ticker symbol.
        current_price (float): The current market price of the stock.
        lower_2_sigma_target (Optional[float]): The lower 2-sigma price target.
        upper_2_sigma_target (Optional[float]): The upper 2-sigma price target.
        currency (str): The currency symbol to use.

    Returns:
        matplotlib.figure.Figure: The generated Matplotlib figure.
    """
    s_values = np.array(strategy_details.get("s_values_for_plot", []))
    pnl_values = np.array(strategy_details.get("pnl_values_for_plot", []))

    # FIX: Add type: ignore to suppress informational warnings on complex library functions
    fig, ax = plt.subplots(figsize=(8, 5)) # type: ignore

    if s_values.size == 0 or pnl_values.size == 0:
        ax.text(0.5, 0.5, "No plotting data available.", ha='center', va='center', fontsize=12, color='red') # type: ignore
        ax.set_title(f"{ticker_symbol} - Strategy P&L") # type: ignore
        return fig

    # --- Plotting logic ---
    ax.plot(s_values, pnl_values, label="P&L at Front Expiry", color="blue", linewidth=1.5) # type: ignore
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.7) # type: ignore
    ax.axvline(x=current_price, color='red', linestyle='--', label=f"Current: {currency}{current_price:.2f}", linewidth=1) # type: ignore

    if lower_2_sigma_target is not None and upper_2_sigma_target is not None:
        ax.axvspan(lower_2_sigma_target, upper_2_sigma_target, alpha=0.1, color='orange', label="2σ Range") # type: ignore
    
    strategy_desc = strategy_details.get('description', 'Strategy P&L')
    ax.set_title(f"{ticker_symbol} - {strategy_desc}", fontsize=11) # type: ignore
    ax.set_xlabel(f"Stock Price at Front Expiration ({currency})", fontsize=10) # type: ignore
    ax.set_ylabel(f"Profit / Loss ({currency})", fontsize=10) # type: ignore
    ax.legend(fontsize=8, loc='best') # type: ignore
    ax.grid(True, which='both', linestyle=':', linewidth=0.5) # type: ignore

    fig.tight_layout(pad=1.0)
    
    return fig