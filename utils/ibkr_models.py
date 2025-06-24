# utils/ibkr_models.py
"""
This module defines strongly-typed data structures for representing data
returned from the Interactive Brokers API. Using these models ensures
type safety throughout the application.
"""
from dataclasses import dataclass
from typing import Dict, Literal, Set, TypedDict

# A typed dictionary for status update callbacks
class StatusPayload(TypedDict):
    """A structured payload for status updates."""
    module: str
    type: Literal["info", "warning", "error", "debug"]
    message: str

# A dataclass to represent a single historical data bar
@dataclass(frozen=True)
class HistoricalBar:
    """Represents a single historical data bar."""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    wap: float
    count: int

# A dataclass for a single portfolio position
@dataclass(frozen=True)
class Position:
    """Represents a single portfolio position."""
    account: str
    symbol: str
    sec_type: str
    currency: str
    con_id: int
    position: float
    average_cost: float

# A dataclass for the account summary
@dataclass(frozen=True)
class AccountSummary:
    """Represents the account summary data."""
    account: str
    tags: Dict[str, str]

# A dataclass for the final status of an order
@dataclass(frozen=True)
class OrderStatus:
    """Represents the terminal status of an order."""
    order_id: int
    status: str
    filled: float
    remaining: float

# A dataclass for option chain parameters
@dataclass(frozen=True)
class OptionChain:
    """Represents the set of expirations and strikes for an option chain."""
    exchange: str
    underlying_con_id: int
    trading_class: str
    multiplier: str
    expirations: Set[str]
    strikes: Set[float]