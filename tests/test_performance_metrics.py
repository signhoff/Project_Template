# tests/test_options_models.py

import pytest
import numpy as np

from utils.options_models import black_scholes_price

def test_black_scholes_call_at_the_money():
    """
    Tests the Black-Scholes formula for a call option that is at-the-money.
    Uses a known online calculator value for validation.
    """
    S = 100  # Stock Price
    K = 100  # Strike Price
    T = 1.0  # Time to expiration (1 year)
    r = 0.05 # Risk-free rate (5%)
    sigma = 0.2 # Volatility (20%)
    
    expected_price = 10.45
    
    calculated_price = black_scholes_price(S, K, T, r, sigma, option_type="call")
    
    # FIX: Suppress the informational warning about the complexity of pytest.approx
    assert calculated_price == pytest.approx(expected_price, abs=0.01) # type: ignore

def test_black_scholes_put_in_the_money():
    """
    Tests the Black-Scholes formula for a put option that is in-the-money.
    """
    S = 90
    K = 100
    T = 0.5 # 6 months
    r = 0.03
    sigma = 0.25
    
    expected_price = 11.74
    
    calculated_price = black_scholes_price(S, K, T, r, sigma, option_type="put")
    
    # FIX: Suppress the informational warning about the complexity of pytest.approx
    assert calculated_price == pytest.approx(expected_price, abs=0.01) # type: ignore

def test_black_scholes_expiration_edge_case():
    """
    Tests the edge case where time to expiration is zero.
    The price should be the intrinsic value.
    """
    call_price = black_scholes_price(S=110, K=100, T=0, r=0.05, sigma=0.2, option_type="call")
    assert call_price == 10.0

    put_price = black_scholes_price(S=90, K=100, T=0, r=0.05, sigma=0.2, option_type="put")
    assert put_price == 10.0

def test_black_scholes_invalid_option_type():
    """
    Tests that the function handles an invalid option type gracefully.
    """
    price = black_scholes_price(100, 100, 1, 0.05, 0.2, option_type="invalid")
    assert np.isnan(price)