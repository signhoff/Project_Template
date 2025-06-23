# handlers/polygon_api_handler_historical.py
import logging
import pandas as pd
from typing import Optional, Callable, Dict, Any, List, TYPE_CHECKING

# This is the correct pattern for providing types for an un-typed library.
# The `if TYPE_CHECKING:` block is read by Pylance, but ignored at runtime.
if TYPE_CHECKING:
    # --- Start of Definitions for Pylance ---
    # We are DEFINING dummy classes here to teach Pylance what the library looks like.
    class NoResultsError(Exception):
        pass

    class Agg:
        timestamp: int
        open: float
        high: float
        low: float
        close: float
        volume: float

    class AsyncRESTClient:
        def __init__(self, api_key: str) -> None: ...
        async def __aenter__(self) -> "AsyncRESTClient": ...
        async def __aexit__(self, *args: Any) -> None: ...
        async def get_aggs(self, **kwargs: Any) -> List[Agg]: ...
    # --- End of Definitions for Pylance ---

# The `else` block is ignored by Pylance but is executed at runtime.
else:
    from polygon import AsyncRESTClient, NoResultsError, Agg

from configs.polygon_config import POLYGON_API_KEY

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    import sys
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s (PolygonAPIHandler) - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False

class PolygonAPIHandlerHistorical:
    """
    Handles asynchronous historical data fetching from Polygon.io using the official
    polygon-api-client library.
    """
    def __init__(self, api_key: Optional[str] = POLYGON_API_KEY, status_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.api_key = api_key
        self.status_callback = status_callback
        self._log_status_message("PolygonAPIHandlerHistorical instance created.")

    def _log_status_message(self, message_text: str, level: str = "INFO", **kwargs: Any) -> None:
        log_level_upper = level.upper()
        if log_level_upper == "ERROR": logger.error(message_text)
        elif log_level_upper == "WARNING": logger.warning(message_text)
        else: logger.info(message_text)
        if self.status_callback:
            try:
                payload = {"type": level.lower(), "module": "PolygonHandler", "message": message_text}
                payload.update(kwargs)
                self.status_callback(payload)
            except Exception as e_cb:
                logger.error(f"Error occurred in Polygon status_callback: {e_cb}", exc_info=True)

    async def get_historical_stock_bars(self, ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        if not self.api_key:
            self._log_status_message("Cannot fetch stock bars: Polygon API key not set.", level="ERROR")
            return None

        self._log_status_message(f"Fetching Polygon stock data for {ticker} from {start_date} to {end_date}...")
        try:
            async with AsyncRESTClient(self.api_key) as client:
                resp: List[Agg] = await client.get_aggs(
                    ticker=ticker.upper(), multiplier=1, timespan="day",
                    from_=start_date, to=end_date, limit=50000,
                )
                if not resp:
                    self._log_status_message(f"No data returned by Polygon for {ticker}.", level="WARNING")
                    return None

                df = pd.DataFrame([vars(agg) for agg in resp])
                df['date'] = pd.to_datetime(df['timestamp'], unit='ms') # type: ignore
                df = df.set_index('date') # type: ignore
                df = df[['open', 'high', 'low', 'close', 'volume']]
                
                self._log_status_message(f"Successfully fetched {len(df)} bars for {ticker}.")
                return df

        except NoResultsError:
            self._log_status_message(f"No data found by Polygon for {ticker} in the specified range.", level="WARNING")
            return None
        except Exception as e:
            self._log_status_message(f"An unexpected error occurred fetching data for {ticker}: {e}", exc_info=True)
            return None
        
