# data_manager.py
import pandas as pd
import os
import logging
from datetime import datetime, timedelta
from typing import Optional

from handlers.polygon_api_handler_historical import PolygonAPIHandlerHistorical

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    import sys
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s (DataManager) - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

class DataManager:
    """
    Manages fetching and caching of historical market data to local storage.
    """
    def __init__(self, data_path: str = 'data/daily/us/stock/', polygon_handler: Optional[PolygonAPIHandlerHistorical] = None):
        self.data_path = data_path
        self.polygon_handler = polygon_handler or PolygonAPIHandlerHistorical()
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            logger.info(f"Created data directory at: {self.data_path}")

    def _get_file_path(self, ticker: str) -> str:
        return os.path.join(self.data_path, f"{ticker.upper()}.parquet")

    async def get_daily_stock_data(self, ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        ticker = ticker.upper()
        file_path = self._get_file_path(ticker)
        
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            logger.error("Invalid date format. Please use YYYY-MM-DD.", exc_info=True)
            return None

        local_df: Optional[pd.DataFrame] = None
        if os.path.exists(file_path):
            try:
                local_df = pd.read_parquet(file_path)
                logger.info(f"Loaded {len(local_df)} rows for {ticker} from local cache.")
            except Exception as e:
                logger.error(f"Failed to read local cache file for {ticker}: {e}", exc_info=True)
                local_df = None

        if local_df is not None and not local_df.empty:
            assert isinstance(local_df.index, pd.DatetimeIndex), "Index must be a DatetimeIndex for date operations."
            last_cached_date = local_df.index[-1].date()

            if end_dt > last_cached_date:
                fetch_start_date = last_cached_date + timedelta(days=1)
                new_data_df = await self.polygon_handler.get_historical_stock_bars(
                    ticker, fetch_start_date.strftime('%Y-%m-%d'), end_date
                )
                if new_data_df is not None and not new_data_df.empty:
                    local_df = pd.concat([local_df, new_data_df])
                    local_df = local_df[~local_df.index.duplicated(keep='last')]
                    self._save_data(ticker, local_df)
            # If data is fresh enough, we just proceed with the existing local_df
        else:
            # No local data, so fetch the full range
            local_df = await self.polygon_handler.get_historical_stock_bars(
                ticker, start_date, end_date
            )
            if local_df is not None and not local_df.empty:
                self._save_data(ticker, local_df)
        
        if local_df is not None and not local_df.empty:
            # Final filtering using the date objects to ensure correctness
            assert isinstance(local_df.index, pd.DatetimeIndex)
            mask = (local_df.index.date >= start_dt) & (local_df.index.date <= end_dt)
            return local_df.loc[mask]
        
        logger.warning(f"Could not retrieve any data for {ticker}.")
        return None

    def _save_data(self, ticker: str, df: pd.DataFrame) -> None:
        file_path = self._get_file_path(ticker)
        try:
            df.to_parquet(file_path, engine='pyarrow')
            logger.info(f"Successfully saved/updated data for {ticker} at {file_path}")
        except Exception as e:
            logger.error(f"Failed to save data for {ticker} to {file_path}: {e}", exc_info=True)

