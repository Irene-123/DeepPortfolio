from typing import List
import datetime
from dataclasses import dataclass, field

from src.models.trade import Trade
from src.models.stock_info import StockInfo


@dataclass
class Holding:
    # Current status
    symbol: str = ""
    quantity: int = 0
    buy_average: float = 0
    investment: float = 0
    current_price: float = 0
    unrealized_profit: float = 0

    # Trade history
    trades: List[Trade] = field(default_factory=list)
    investment_trend: list = field(default_factory=list)
    quantity_trend: list = field(default_factory=list)
    realized_profit_history: list = field(default_factory=list)
    dividend_history: list = field(default_factory=list)

    # Past performance
    realized_profit: float = 0
    dividend_income: float = 0

    # Performance metrics
    risk_free_return_trend: list = field(default_factory=list)
    nifty50_return_trend: list = field(default_factory=list)
    bsesensex_return_trend: list = field(default_factory=list)
    niftybank_return_trend: list = field(default_factory=list)
    
    # Stock information
    stock_info: StockInfo = None