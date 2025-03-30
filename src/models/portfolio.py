from typing import List
from dataclasses import dataclass, field

from src.models.holding import Holding
from src.models.stock_info import StockInfo

@dataclass
class Portfolio:
    stocks: List[StockInfo]
    holdings: List[Holding]

    # Investment Metrics =========================================================
    total_investment: float = 0 # Total investment
    current_value: float = 0 # Current value of the portfolio
    profit_loss: float = 0 # Profit or loss
    yield_on_cost: float = 0 # Yield on cost

    # Income Metrics =============================================================
    dividend_yield: float = 0
    average_dividend_yield: float = 0
    weighted_average_dividend_yield: float = 0 # Weighted average dividend yield

    # Valuation Metrics ==========================================================
    trailing_pe: float = 0
    forward_pe: float = 0
    weighted_average_price_to_book: float = 0 # Weighted average price-to-book ratio
    weighted_average_price_to_sales: float = 0 # Weighted average price-to-sales ratio
    weighted_average_enterprise_to_revenue: float = 0 # Weighted average enterprise-to-revenue ratio
    weighted_average_enterprise_to_ebitda: float = 0 # Weighted average enterprise-to-EBITDA ratio
    weighted_average_target_price: float = 0 # Weighted average target price

    # Risk Metrics ===============================================================
    beta: float = 0 # Portfolio beta
    weighted_average_beta: float = 0 # Weighted average beta of stocks
    sharpe_ratio: float = 0 # Sharpe ratio of the portfolio
    sortino_ratio: float = 0 # Sortino ratio of the portfolio
    alpha: float = 0 # Portfolio alpha
    standard_deviation: float = 0 # Standard deviation of returns
    max_drawdown: float = 0 # Maximum drawdown
    annualized_volatility: float = 0 # Annualized volatility of the portfolio
    tracking_error: float = 0 # Tracking error against a benchmark

    # Performance Metrics ========================================================
    annualized_return: float = 0 # Annualized return of the portfolio
    information_ratio: float = 0 # Information ratio against a benchmark
    turnover_ratio: float = 0 # Portfolio turnover ratio

    # Allocation Metrics =========================================================
    sector_weights: dict[str, dict[str, float]] = field(default_factory=dict) # Sector weights
    industry_weights: dict[str, dict[str, float]] = field(default_factory=dict) # Industry weights
    concentration_ratio: float = 0 # Portfolio concentration ratio
    weighted_average_market_cap: float = 0 # Weighted average market cap of holdings

    # Profitability Metrics ======================================================
    weighted_average_ebitda_margin: float = 0 # Weighted average EBITDA margin
    weighted_average_operating_margin: float = 0 # Weighted average operating margin
    weighted_average_gross_margin: float = 0 # Weighted average gross margin

    # Growth Metrics =============================================================
    weighted_average_revenue_growth: float = 0 # Weighted average revenue growth
    weighted_average_eps_growth: float = 0 # Weighted average EPS growth
    weighted_average_earnings_growth: float = 0 # Weighted average earnings growth

    # Leverage Metrics ===========================================================
    weighted_average_debt_to_equity: float = 0 # Weighted average debt-to-equity ratio