# handlers/yfinance_handler.py
"""
Handles historical data fetching from the yfinance library.
"""

import logging
import pandas as pd
import yfinance as yf
from typing import Optional, Dict, Any

# Inherits the central logging configuration
logger = logging.getLogger(__name__)

class YFinanceHandler:
    """
    A handler for fetching historical stock data and ticker information
    using the yfinance library.
    """
    def get_historical_stock_bars(
        self,
        ticker: str,
        start_date: str,
        end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        Fetches historical daily bars for a stock ticker using yfinance.

        Args:
            ticker (str): The stock ticker symbol.
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.

        Returns:
            Optional[pd.DataFrame]: DataFrame with OHLCV data, or None if an error occurs.
        """
        logger.info(f"Fetching yfinance historical data for {ticker} from {start_date} to {end_date}...")
        try:
            data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)

            if data.empty:
                logger.warning(f"No historical data returned by yfinance for {ticker} in the specified range.")
                return None

            data.rename(columns={
                'Open': 'open', 'High': 'high', 'Low': 'low',
                'Close': 'close', 'Volume': 'volume'
            }, inplace=True)
            
            data.index.name = 'date'

            logger.info(f"Successfully fetched {len(data)} bars for {ticker} from yfinance.")
            return data[['open', 'high', 'low', 'close', 'volume']]

        except Exception as e:
            logger.error(f"An unexpected error occurred fetching historical data for {ticker} from yfinance: {e}", exc_info=True)
            return None

    def get_ticker_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Fetches fundamental information for a given stock ticker.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing ticker information
            (like marketCap, sector, etc.), or None if the ticker is invalid.
        """
        logger.info(f"Fetching ticker info for {ticker} from yfinance...")
        try:
            ticker_obj = yf.Ticker(ticker)
            info_dict = ticker_obj.info

            # yfinance returns a dict with a 'trailingPegRatio' of None for invalid tickers.
            # We check for a more reliable key like 'symbol' to validate.
            if not info_dict or info_dict.get('symbol') != ticker.upper():
                 logger.warning(f"Could not retrieve valid info for ticker '{ticker}'. It may be delisted or invalid.")
                 return None

            logger.info(f"Successfully fetched info for {ticker}.")
            return info_dict

        except Exception as e:
            logger.error(f"An unexpected error occurred fetching info for {ticker} from yfinance: {e}", exc_info=True)
            return None