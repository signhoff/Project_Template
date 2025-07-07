# Quantitative Finance Project Template

This repository serves as a professional, scalable template for quantitative finance applications in Python. It provides a robust architecture for developing, testing, and deploying strategies that interact with financial data APIs like Interactive Brokers and Polygon.io.

## Core Features

* **Asynchronous API Handling**: Built with `asyncio` for high-performance, non-blocking interactions with real-time data sources.
* **Multi-Source Data Integration**: Includes handlers for Interactive Brokers (TWS API), Polygon.io, and yfinance, designed for easy extension.
* **Intelligent Data Caching**: The `DataManager` minimizes redundant API calls by caching historical data locally in the efficient Parquet format.
* **Modular Utilities**: A rich set of utility modules for financial calculations (e.g., Black-Scholes), performance metrics (e.g., Sharpe Ratio), and plotting.
* **Secure Configuration**: Manages API keys and sensitive settings securely through environment variables using a `.env` file.
* **Centralized Logging**: A pre-configured logging setup that provides consistent and clear output across all modules.
* **Testing Framework**: Includes a `pytest` environment with existing unit tests for core utilities, promoting a test-driven development approach.

---

## Project Structure
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
│   └── plotting_utils.py
│   └── polygon_utils.py
│   └── financial_calculations.py
├── .env                    # Local environment variables (API keys, etc.)
├── .gitignore              # Specifies files for Git to ignore
├── .python-version         # Specifies the python version for pyenv users
├── data_manager.py         # Core class for managing data access and caching
├── pyproject.toml          # Project metadata and dependencies
└── requirements.txt        # List of Python package dependencies

---

## Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # You may need to adjust your execution policy for the current process
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    .\venv\Scripts\Activate.ps1
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

5.  **Configure VS Code Interpreter:**
    * Use `Ctrl+Shift+P` to open the command palette.
    * Search for and select **Python: Select Interpreter**.
    * Choose the Python executable from your virtual environment (e.g., `.\venv\Scripts\python.exe`).

---

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

---

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

---

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

---

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

=========================================
THIS MUST BE DONE IN WINDOWS POERSHELL
=========================================
## Your Personal Git & GitHub Workflow Guide

Here are the standard command-line steps for managing your projects with Git and GitHub.

Before you start:
    See what remote repository your local project is currently pointing to by running
      git remote -v
    If applicable, remove the wrong remote link
      git remote remove origin
    Add the correct remote URL
      git remote add origin https://github.com/signhoff/Quantitative_Momentum
    Push to the correct repository
      git push -u origin main

### **Part 1: How to Upload a Brand New Project to GitHub**

  Step 1: CD into the Project Folder
    cd "C:\Users\17082\Documents\TWS_Projects\Project_Template\"

  Step 2: Initialize Git and Make Your First "Commit"
    # 1. git init
    # 2. git add .
    # 3. git commit -m "Initial commit"

  Step 3: Create the GitHub Repository and Push
    gh repo create
    ***answer any questions***

***First-Time Setup Note:** If you ever get an `Author identity unknown` error after the `git commit` command,
run these two commands one time to set up your identity, then try the `git commit` command again:***
  `git config --global user.name "YourGitHubUsername"`
  `git config --global user.email "your_email_for_github@example.com"`

### **Part 2: Push Updates to an Existing Project**

  Step 1: CD into Your Project Folder
      cd "C:\Users\17082\Documents\TWS_Projects\Project_Template\"

  Step 2: Check the Status of Your Changes**
    This is the most common command you'll use. It shows you which files you have modified, added, or deleted.
    Files in **red** are changes that have not yet been prepared ("staged") for the next commit.
      git status
    
  Step 3: Add Your Changes to the Staging Area
  You need to tell Git exactly which changes you want to include in the next update.

    # To add ALL changes you've made:
      git add .

    # OR, to add changes from a specific file only:
      git add "C:\Users\17082\Documents\TWS_Projects\Project_Template\[folder/file name]"

After running `git add`, if you run `git status` again, you'll see the files have turned **green**. This means
they are "staged" and ready to be committed.

  Step 4: Commit Your Staged Changes
    Bundle your staged changes into a "commit" with a clear message describing what you did.
    Write a clear, descriptive message inside the quotes
      git commit -m "Add new feature for user profiles"

*Good commit messages are very helpful\! Examples: "Fix bug on the login page", "Update documentation for API",
"Add historical data for 2024".*

  Step 5: Push Your Commit to GitHub

This sends all of your new, committed changes from your local computer up to your GitHub repository.
  git push
  
git remote add origin https://github.com/signhoff/Project_Template.git
git branch -M main
git push -u origin main

git push origin main --force <- this will override everything watch out if you are using this
