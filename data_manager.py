# data_manager.py
import pandas as pd
import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Union

from handlers.polygon_api_handler_historical import PolygonAPIHandlerHistorical
from handlers.yfinance_handler import YFinanceHandler

logger = logging.getLogger(__name__)

class DataManager:
    """
    Manages fetching and caching of historical market data to local storage.
    Supports multiple data sources like Polygon and yfinance.
    """
    def __init__(
        self,
        data_path: str = 'data/',
        polygon_handler: Optional[PolygonAPIHandlerHistorical] = None,
        yfinance_handler: Optional[YFinanceHandler] = None
    ):
        """
        Initializes the DataManager.

        Args:
            data_path (str): The base path for all cached data.
            polygon_handler (Optional[PolygonAPIHandlerHistorical]): An instance of the Polygon handler.
            yfinance_handler (Optional[YFinanceHandler]): An instance of the yfinance handler.
        """
        self.base_data_path = data_path
        self.polygon_handler = polygon_handler or PolygonAPIHandlerHistorical()
        self.yfinance_handler = yfinance_handler or YFinanceHandler()
        if not os.path.exists(self.base_data_path):
            os.makedirs(self.base_data_path)
            logger.info(f"Created base data directory at: {self.base_data_path}")

    def _get_file_path(self, ticker: str, source: str) -> str:
        """
        Constructs the full path for a ticker's data file, including the source.
        Example: data/polygon/daily/SPY.parquet
        """
        source_path = os.path.join(self.base_data_path, source, 'daily')
        if not os.path.exists(source_path):
            os.makedirs(source_path)
        return os.path.join(source_path, f"{ticker.upper()}.parquet")

    async def get_daily_stock_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        source: str = 'polygon'
    ) -> Optional[pd.DataFrame]:
        """
        Retrieves daily stock data for a given ticker and date range.
        It loads from the local cache and fetches missing data from the specified API source.

        Args:
            ticker (str): The stock ticker symbol.
            start_date (str): The start date in 'YYYY-MM-DD' format.
            end_date (str): The end date in 'YYYY-MM-DD' format.
            source (str): The data source ('polygon' or 'yfinance'). Defaults to 'polygon'.

        Returns:
            Optional[pd.DataFrame]: A DataFrame with the requested data, or None.
        """
        file_path = self._get_file_path(ticker, source)
        
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
                logger.info(f"Loaded {len(local_df)} rows for {ticker} from local cache ({source}).")
            except Exception as e:
                logger.error(f"Failed to read local cache file for {ticker}: {e}", exc_info=True)
                local_df = None

        handler: Union[PolygonAPIHandlerHistorical, YFinanceHandler]
        if source.lower() == 'polygon':
            handler = self.polygon_handler
        elif source.lower() == 'yfinance':
            handler = self.yfinance_handler
        else:
            logger.error(f"Invalid data source '{source}'. Choose 'polygon' or 'yfinance'.")
            return None

        if local_df is not None and not local_df.empty:
            assert isinstance(local_df.index, pd.DatetimeIndex), "Index must be a DatetimeIndex"
            last_cached_date = local_df.index[-1].date()
            if end_dt > last_cached_date:
                fetch_start_date = last_cached_date + timedelta(days=1)
                
                # The yfinance handler is synchronous, so we await conditionally
                if isinstance(handler, PolygonAPIHandlerHistorical):
                    new_data_df = await handler.get_historical_stock_bars(
                        ticker, fetch_start_date.strftime('%Y-%m-%d'), end_date
                    )
                else:
                    new_data_df = handler.get_historical_stock_bars(
                        ticker, fetch_start_date.strftime('%Y-%m-%d'), end_date
                    )
                
                if new_data_df is not None and not new_data_df.empty:
                    local_df = pd.concat([local_df, new_data_df])
                    local_df = local_df[~local_df.index.duplicated(keep='last')]
                    self._save_data(ticker, source, local_df)
        else:
            # No local data, so fetch the full range
            if isinstance(handler, PolygonAPIHandlerHistorical):
                local_df = await handler.get_historical_stock_bars(ticker, start_date, end_date)
            else:
                local_df = handler.get_historical_stock_bars(ticker, start_date, end_date)

            if local_df is not None and not local_df.empty:
                self._save_data(ticker, source, local_df)
        
        if local_df is not None and not local_df.empty:
            assert isinstance(local_df.index, pd.DatetimeIndex)
            mask = (local_df.index.date >= start_dt) & (local_df.index.date <= end_dt)
            return local_df.loc[mask]
        
        logger.warning(f"Could not retrieve any data for {ticker} from {source}.")
        return None

    def _save_data(self, ticker: str, source: str, df: pd.DataFrame) -> None:
        """Saves a DataFrame to a Parquet file in the correct source directory."""
        file_path = self._get_file_path(ticker, source)
        try:
            df.to_parquet(file_path, engine='pyarrow')
            logger.info(f"Successfully saved/updated data for {ticker} at {file_path}")
        except Exception as e:
            logger.error(f"Failed to save data for {ticker} to {file_path}: {e}", exc_info=True)
