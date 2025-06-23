# Quantitative Finance Project Template

This repository serves as a robust, professional-grade template for developing quantitative finance applications in Python. It provides a clean architecture with a strong separation of concerns, featuring modular components for API interaction, data management, financial calculations, and testing.

## Core Features

* **Asynchronous API Handling**: Utilizes `asyncio` for high-performance, non-blocking interaction with the Interactive Brokers API.
* **Local Data Caching**: Features a `DataManager` that intelligently caches historical data from APIs to local Parquet files, dramatically speeding up subsequent data requests and managing API rate limits.
* **Multi-Source Data Integration**: Seamlessly fetch historical data from different providers (Polygon.io, yfinance) through a unified interface.
* **Modular Utilities**: A clean `utils` directory with separate modules for options pricing models, performance metrics, and plotting helpers.
* **Secure Configuration**: Uses a `.env` file for secure management of API keys, keeping secrets out of source code.
* **Centralized Logging**: A single utility configures logging for the entire application, ensuring consistent and readable log output for easy debugging.
* **Testing Framework**: Includes a `tests/` directory with `pytest` configured, complete with examples for testing financial calculations.

## Project Structure

```
/
├── configs/                # Configuration files for APIs and application settings
│   ├── ibkr_config.py
│   └── polygon_config.py
├── data/                   # Local cache for historical data (ignored by Git)
├── handlers/               # Modules for interacting with external APIs
│   ├── ibkr_api_wrapper.py
│   ├── ibkr_base_handler.py
│   ├── ibkr_option_handler.py
│   ├── ibkr_stock_handler.py
│   ├── polygon_api_handler_historical.py
│   └── yfinance_handler.py
├── tests/                  # Unit and integration tests
│   ├── test_options_models.py
│   └── test_performance_metrics.py
├── utils/                  # Reusable, pure-logic utility functions
│   ├── logging_config.py
│   ├── options_models.py
│   ├── performance_metrics.py
│   ├── plotting_utils.py
│   └── polygon_utils.py
├── .env                    # Local environment variables (API keys, etc.)
├── .gitignore              # Specifies files for Git to ignore
├── data_manager.py         # Core class for managing data access and caching
├── pyproject.toml          # Project metadata and dependencies
└── requirements.txt        # List of Python package dependencies
```

## Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the IBKR TWS API**
    This project requires the official TWS API from Interactive Brokers. You must install it from the local source file.
    *(Instructions from your `Setup_Instructions.txt`)*
    ```bash
    python -m pip install --upgrade "C:\TWS API\source\pythonclient\dist\ibapi-10.30.1-py3-none-any.whl"
    ```

4.  **Install Python Dependencies**
    Install all required packages from the `requirements.txt` file.
    ```bash
    python -m pip install -r requirements.txt
    ```

## Configuration

### 1. API Keys

This project uses a `.env` file to securely store your API keys.

1.  Create a file named `.env` in the project root directory.
2.  Add your Polygon.io API key to this file:
    ```
    POLYGON_API_KEY="YOUR_POLYGON_API_KEY_HERE"
    ```

### 2. Interactive Brokers (TWS / Gateway)

For the IBKR handlers to connect, you must have either Trader Workstation (TWS) or the IBKR Gateway running.

1.  In TWS/Gateway, go to **File > Global Configuration**.
2.  Select **API > Settings** from the left pane.
3.  Ensure **"Enable ActiveX and Socket Clients"** is checked.
4.  Make note of the **"Socket port"** number. The default is `7497` for TWS paper trading, which matches the default in `configs/ibkr_config.py`.
5.  It is recommended to add `127.0.0.1` to the list of **"Trusted IP Addresses"**.

## Module Usage Guide

This template is designed to be used as a collection of powerful, independent modules. You would typically import and use them in a central `main.py` application script.

### `DataManager` (Primary Historical Data Access)

The `DataManager` is the main entry point for getting historical bar data. It will automatically cache data to prevent re-calling APIs.

**Note on Polygon.io Rate Limiting:** The free tier for Polygon's API is limited to 5 calls per minute. The `DataManager` is essential for managing this, as it will only call the API for dates not present in your local cache.

```python
import asyncio
from data_manager import DataManager

async def main():
    data_manager = DataManager()

    # Get 1 year of SPY data from Polygon (will be cached locally)
    spy_data_poly = await data_manager.get_daily_stock_data(
        ticker='SPY',
        start_date='2023-01-01',
        end_date='2024-01-01',
        source='polygon'  # Specify the source
    )
    if spy_data_poly is not None:
        print("--- Polygon Data for SPY ---")
        print(spy_data_poly.tail())
```

### Direct Handler Usage (for non-historical data)

While the `DataManager` is best for historical bars, you can use handlers directly for other types of information.

#### `yfinance_handler.py`
The `YFinanceHandler` can be used to get fundamental company information.

```python
from handlers.yfinance_handler import YFinanceHandler

def get_info():
    yf_handler = YFinanceHandler()
    
    # Get fundamental info for a ticker
    nvda_info = yf_handler.get_ticker_info("NVDA")
    
    if nvda_info:
        market_cap = nvda_info.get("marketCap")
        sector = nvda_info.get("sector")
        print(f"\n--- Ticker Info for NVDA ---")
        print(f"Market Cap: {market_cap:,}")
        print(f"Sector: {sector}")

# To run this synchronous function:
# get_info()
```

### Calculation Utilities

The `utils` modules contain pure functions for analysis.

#### `options_models.py`
```python
from utils.options_models import black_scholes_price

# Calculate the price of a call option
price = black_scholes_price(S=150, K=155, T=0.25, r=0.05, sigma=0.22, option_type='call')
print(f"\nCalculated Call Price: {price:.2f}")
```

#### `performance_metrics.py`
```python
from utils.performance_metrics import calculate_sharpe_ratio
# Assuming 'spy_data_poly' is a DataFrame from the DataManager
# daily_returns = spy_data_poly['close'].pct_change().dropna()
# sharpe = calculate_sharpe_ratio(daily_returns, risk_free_rate=0.05)
# print(f"SPY Sharpe Ratio: {sharpe:.2f}")
```

## Running the Test Suite

This project uses `pytest`. To run all tests and ensure the core logic is working correctly, navigate to the project root in your terminal and simply run:

```bash
pytest
```