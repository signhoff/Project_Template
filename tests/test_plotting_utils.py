# tests/test_plotting_utils.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any

# FIX: Import Figure directly from the correct module
from matplotlib.figure import Figure

from utils.plotting_utils import create_pnl_figure

def test_create_pnl_figure_with_valid_data():
    """
    Tests that the function returns a valid Matplotlib Figure and sets titles
    and labels correctly when given proper data.
    """
    # FIX: Add an explicit type hint to the dictionary
    strategy_details: Dict[str, Any] = {
        "s_values_for_plot": np.linspace(80, 120, 50),
        "pnl_values_for_plot": np.random.randn(50) * 100,
        "description": "Test Strategy"
    }
    ticker = "TEST"
    current_price = 100.0
    
    fig = create_pnl_figure(strategy_details, ticker, current_price, 90, 110)

    # FIX: Check against the correctly imported Figure class
    assert isinstance(fig, Figure)

    ax = fig.axes[0]
    assert ax.get_title() == "TEST - Test Strategy"
    assert ax.get_xlabel() == "Stock Price at Front Expiration ($)"
    assert ax.get_ylabel() == "Profit / Loss ($)"
    
    assert len(ax.get_lines()) > 0

    plt.close(fig)

def test_create_pnl_figure_with_empty_data():
    """
    Tests that the function handles empty data gracefully without crashing and
    displays the appropriate message.
    """
    # FIX: Add an explicit type hint to the dictionary
    strategy_details: Dict[str, Any] = {
        "s_values_for_plot": [],
        "pnl_values_for_plot": []
    }
    ticker = "EMPTY"
    current_price = 100.0

    fig = create_pnl_figure(strategy_details, ticker, current_price, 90, 110)

    # FIX: Check against the correctly imported Figure class
    assert isinstance(fig, Figure)

    ax = fig.axes[0]
    
    assert len(ax.get_lines()) == 0
    assert len(ax.texts) > 0
    assert ax.texts[0].get_text() == "No plotting data available."

    plt.close(fig)