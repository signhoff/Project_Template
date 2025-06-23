# stubs/polygon/__init__.pyi
# This file provides a more complete set of type hints for the polygon-api-client library.

from typing import Any, List, Optional, AsyncContextManager

# Define the structure of the exception
class NoResultsError(Exception): ...

# Define the structure of the Aggregate data object
class Agg:
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: float
    timestamp: int
    transactions: int
    otc: Optional[bool]

# Define the structure of the AsyncRESTClient
class AsyncRESTClient(AsyncContextManager["AsyncRESTClient"]):
    def __init__(self, api_key: str, timeout: int = ...) -> None: ...

    async def get_aggs(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        from_: str,
        to: str,
        **kwargs: Any
    ) -> List[Agg]: ...
    
    async def close(self) -> None: ...