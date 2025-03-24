from typing import List
from dataclasses import dataclass

from models.holding import Holding
from models.stock_info import StockInfo

@dataclass
class Portfolio:
    stocks: List[StockInfo]
    holdings: List[Holding]

    # Investment Metrics =========================================================
    total_investment: float # Total investment
    current_value: float # Current value of the portfolio
    profit_loss: float # Profit or loss
    yield_on_cost: float # Yield on cost

    # Income Metrics =============================================================
    dividend_yield: float
    average_dividend_yield: float
    weighted_average_dividend_yield: float # Weighted average dividend yield

    # Valuation Metrics ==========================================================
    trailing_pe: float
    forward_pe: float
    weighted_average_price_to_book: float # Weighted average price-to-book ratio
    weighted_average_price_to_sales: float # Weighted average price-to-sales ratio
    weighted_average_enterprise_to_revenue: float # Weighted average enterprise-to-revenue ratio
    weighted_average_enterprise_to_ebitda: float # Weighted average enterprise-to-EBITDA ratio
    weighted_average_target_price: float # Weighted average target price

    # Risk Metrics ===============================================================
    beta: float # Portfolio beta
    weighted_average_beta: float # Weighted average beta of stocks
    sharpe_ratio: float # Sharpe ratio of the portfolio
    sortino_ratio: float # Sortino ratio of the portfolio
    alpha: float # Portfolio alpha
    standard_deviation: float # Standard deviation of returns
    max_drawdown: float # Maximum drawdown
    annualized_volatility: float # Annualized volatility of the portfolio
    tracking_error: float # Tracking error against a benchmark

    # Performance Metrics ========================================================
    annualized_return: float # Annualized return of the portfolio
    information_ratio: float # Information ratio against a benchmark
    turnover_ratio: float # Portfolio turnover ratio

    # Allocation Metrics =========================================================
    sector_weights: dict[str, dict[str, float]] # Sector weights
    industry_weights: dict[str, dict[str, float]] # Industry weights
    concentration_ratio: float # Portfolio concentration ratio
    weighted_average_market_cap: float # Weighted average market cap of holdings

    # Profitability Metrics ======================================================
    weighted_average_ebitda_margin: float # Weighted average EBITDA margin
    weighted_average_operating_margin: float # Weighted average operating margin
    weighted_average_gross_margin: float # Weighted average gross margin

    # Growth Metrics =============================================================
    weighted_average_revenue_growth: float # Weighted average revenue growth
    weighted_average_eps_growth: float # Weighted average EPS growth
    weighted_average_earnings_growth: float # Weighted average earnings growth

    # Leverage Metrics ===========================================================
    weighted_average_debt_to_equity: float # Weighted average debt-to-equity ratio