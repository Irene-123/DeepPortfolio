import datetime
from dataclasses import dataclass, field
from typing import List

@dataclass
class StockSplit:
    split_date: datetime.date
    ratio: float

@dataclass
class Dividend:
    ex_date: datetime.date
    amount: float
    
@dataclass
class StockInfo:
    # Basic Information ==========================================================
    symbol: str     # NSE symbol for the stock
    symbol_yf: str  # Yahoo Finance symbol for the stock
    name: str       # Name of the company
    city: str       # City where the company is located
    industry: str   # Industry the company operates in
    sector: str     # Sector the company operates in

    # Price and Volume ===========================================================
    previous_close: float           # Previous day's closing price
    volume: int                     # Volume of shares traded
    average_volume_10days: int      # Average volume over the last 10 days
    average_volume_3months: int     # Average volume over the last 3 months
    fifty_two_week_low: float       # 52-week low price
    fifty_two_week_high: float      # 52-week high price
    fifty_two_week_change: float    # 52-week price change

    # Valuation Metrics ==========================================================
    market_cap: int                             # Market capitalization
    book_value: float                           # Book value
    price_to_sales_trailing_12_months: float    # Price to sales ratio
    price_to_book: float                        # Price to book ratio
    trailing_pe: float                          # Trailing P/E ratio
    forward_pe: float                           # Forward P/E ratio
    trailing_eps: float                         # Trailing EPS
    forward_eps: float                          # Forward EPS
    price_eps_current_year: float               # Price to EPS current year

    # Moving Averages ============================================================
    fifty_day_average: float        # 50-day moving average
    two_hundred_day_average: float  # 200-day moving average

    # Financial Ratios ===========================================================
    beta: float                     # Beta value
    debt_to_equity: float           # Debt to equity ratio
    enterprise_to_revenue: float    # Enterprise to revenue ratio
    enterprise_to_ebitda: float     # Enterprise to EBITDA ratio

    # Financial Performance ======================================================
    ebitda: int                     # EBITDA
    total_debt: int                 # Total debt
    total_revenue: int              # Total revenue
    revenue_per_share: float        # Revenue per share
    gross_profit: int               # Gross profit
    revenue_growth: float           # Revenue growth
    gross_margins: float            # Gross margins
    ebitda_margins: float           # EBITDA margins
    operating_margins: float        # Operating margins
    eps_trailing_12months: float    # EPS trailing 12 months
    eps_forward: float              # EPS forward
    eps_current_year: float         # EPS current year

    # Price Targets ==============================================================
    target_high_price: float    # Target high price
    target_low_price: float     # Target low price
    target_mean_price: float    # Target mean price

    # Dividends ==================================================================
    dividend_yield: float                       # Dividend yield
    five_year_average_dividend_yield: float     # Five year average dividend yield

    # Corporate Actions ==========================================================
    stock_splits: List[StockSplit] = field(default_factory=list)
    dividends: List[Dividend] = field(default_factory=list)
