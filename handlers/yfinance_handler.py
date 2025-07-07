# handlers/yfinance_handler.py

"""
Handles historical data fetching from the yfinance library using a
class-based and asynchronous approach for maximum performance.
"""

import asyncio
import os
import sys
from typing import Any, Dict, List, Optional

import pandas as pd
import yfinance as yf

from utils.logging_config import get_logger

logger = get_logger(__name__)

CACHE_DIR = "data/cache"
CACHE_START_DATE = "2000-01-01"


class YFinanceHandler:
    """
    A handler for fetching and caching historical stock data using yfinance.
    Optimized for handling multiple tickers efficiently and asynchronously.
    """

    def __init__(self, cache_dir: str = CACHE_DIR):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.semaphore = asyncio.Semaphore(5)  # Allow a few concurrent info lookups

    async def get_ticker_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Fetches fundamental information for a given stock ticker asynchronously.

        Args:
            ticker (str): The stock ticker symbol.

        Returns:
            A dictionary containing ticker information, or None if invalid.
        """
        async with self.semaphore:
            try:
                # yf.Ticker is a blocking call, so we run it in a thread
                ticker_obj = await asyncio.to_thread(yf.Ticker, ticker)
                info_dict = await asyncio.to_thread(getattr, ticker_obj, 'info')

                if not info_dict or 'symbol' not in info_dict:
                    logger.warning(f"Could not retrieve valid info for ticker '{ticker}'.")
                    return None
                return info_dict
            except Exception as e:
                logger.error(f"An error occurred fetching info for {ticker}: {e}")
                return None

    async def _fetch_and_cache_ticker(self, ticker: str, end_date: str) -> bool:
        """
        Fetches a long history for a single ticker and saves it to a Parquet file.
        Uses a semaphore and a retry mechanism to handle network errors.
        """
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            # Use a tighter semaphore for downloads as they are more intensive
            async with asyncio.Semaphore(1):
                try:
                    ticker_data = await asyncio.to_thread(
                        yf.download,
                        ticker,
                        start=CACHE_START_DATE,
                        end=end_date,
                        auto_adjust=True,
                        progress=False,
                    )

                    if ticker_data.empty:
                        return False

                    if not ticker_data.index.is_unique:
                        logger.warning(f"Duplicate dates found for {ticker}. Keeping last.")
                        ticker_data = ticker_data[~ticker_data.index.duplicated(keep='last')]

                    file_path = os.path.join(self.cache_dir, f"{ticker}.parquet")
                    await asyncio.to_thread(ticker_data.to_parquet, file_path)
                    return True

                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {ticker}: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                    else:
                        logger.error(f"Could not fetch data for {ticker} after {max_retries} attempts.")
                        return False
        return False

    async def get_historical_closes(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> Optional[pd.DataFrame]:
        """
        Asynchronously fetches historical adjusted close prices for a list of tickers,
        utilizing a robust Parquet-based cache.
        """
        all_series = []
        tickers_to_fetch = [
            t for t in tickers if not os.path.exists(os.path.join(self.cache_dir, f"{t}.parquet"))
        ]
        
        if tickers_to_fetch:
            logger.info(f"Cache miss for {len(tickers_to_fetch)} tickers. Fetching now...")
            for i, ticker in enumerate(tickers_to_fetch):
                status_msg = f"--> Fetching {i + 1}/{len(tickers_to_fetch)}: {ticker.ljust(10)}"
                sys.stdout.write(f"\r{status_msg}")
                sys.stdout.flush()
                await self._fetch_and_cache_ticker(ticker, end_date)
            sys.stdout.write("\n")

        logger.info("Loading data from cache and slicing to requested date range...")
        for i, ticker in enumerate(tickers):
            status_msg = f"--> Loading ticker data {i + 1}/{len(tickers)}: {ticker.ljust(10)}"
            sys.stdout.write(f"\r{status_msg}")
            sys.stdout.flush()

            file_path = os.path.join(self.cache_dir, f"{ticker}.parquet")
            if os.path.exists(file_path):
                try:
                    data = await asyncio.to_thread(pd.read_parquet, file_path)
                    series = data["Close"].loc[start_date:end_date]
                    series.name = ticker
                    all_series.append(series)
                except Exception as e:
                    logger.error(f"Failed to read or slice cache for {ticker}: {e}")
        
        sys.stdout.write("\n")
        
        if not all_series:
            return None

        return pd.concat(all_series, axis=1)
