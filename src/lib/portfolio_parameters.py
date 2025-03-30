import datetime
import pandas as pd
from typing import List, Dict

from src.models.trade import Trade
from src.models.portfolio import Portfolio
from src.models.holding import Holding
from src.models.stock_info import StockInfo


def calculate_max_drawdown(investment_trend: list):
    """
    Calculates the maximum drawdown from the investment trend.
    Args:
        investment_trend (list): List of tuples (date, value).
    Returns:
        float: Maximum drawdown as a percentage.
    """
    max_drawdown = 0
    peak = investment_trend[0][1]  # Start with the first value

    for _, value in investment_trend:
        peak = max(peak, value)
        drawdown = (peak - value) / peak
        max_drawdown = max(max_drawdown, drawdown)

    return max_drawdown

def calculate_standard_deviation(investment_trend: List):
    """
    Calculates the standard deviation of returns from the investment trend.
    Args:
        investment_trend (List): List of tuples (date, value).
    Returns:
        float: Standard deviation of returns.
    """
    if len(investment_trend) < 2:
        return 0.0

    returns = []
    for i in range(1, len(investment_trend)):
        previous_value = investment_trend[i - 1][1]
        current_value = investment_trend[i][1]

        # Calculate return for the period
        if previous_value > 0:
            return_value = (current_value - previous_value) / previous_value
            returns.append(return_value)

    # Calculate standard deviation of returns
    if returns:
        return pd.Series(returns).std()
    return 0.0



def compute_monthly_investment_trend(holding: Holding):
    """
    Computes the monthly investment trend for a holding.
    Args:
        holding (Holding): The holding object.
    Returns:
        None: Updates the holding's investment_trend attribute.
    """
    # Ensure investment trend is sorted by date
    investment_trend_df = pd.DataFrame(holding.investment_trend, columns=['date', 'value'])
    investment_trend_df['date'] = pd.to_datetime(investment_trend_df['date'])
    investment_trend_df = investment_trend_df.sort_values('date')

    # Group by month and take the last value of each month
    monthly_trend = investment_trend_df.resample('M', on='date').last().ffill()

    # Update the holding's investment_trend with the monthly trend
    return monthly_trend.reset_index()[['date', 'value']].values.tolist()


def portfolio_parameters(holdings: List[Holding], stock_info: Dict[str, StockInfo]) -> Portfolio:
    """
    This function calculates several portfolio parameters
    E.g.: 
        - Portfolio Value
        - Portfolio Gain/Loss
        - Portfolio Gain/Loss Percentage
        - Portfolio Dividend Yield
        - Portfolio Dividend Yield Percentage
        - Portfolio Dividend Amount
    """
    portfolio = Portfolio(holdings=holdings, stocks=stock_info.values())

    # Example risk-free rate (annualized, e.g., 3%)
    risk_free_rate = 0.03
    portfolio_returns = []
    downside_returns = []

    for holding in holdings:
        symbol = holding.symbol
        stock = stock_info.get(symbol)
        price_to_book = stock.price_to_book if stock else 0
        target_price = stock.target_high_price if stock else 0
        trailing_pe = stock.trailing_pe if stock else 0
        price_to_sales = stock.price_to_sales_trailing_12_months if stock else 0
        enterprise_to_revenue = stock.enterprise_to_revenue if stock else 0
        beta = stock.beta if stock else 0
        forward_pe = stock.forward_pe if stock else 0

        investment_trend = compute_monthly_investment_trend(holding)
        print(investment_trend)

        portfolio.total_investment += holding.buy_average * holding.quantity
        portfolio.current_value += holding.current_price * holding.quantity
        portfolio.dividend_yield += holding.dividend_income * holding.quantity
        portfolio.weighted_average_dividend_yield += (
            holding.dividend_income * holding.quantity / portfolio.current_value
            if portfolio.current_value > 0
            else 0
        )
        portfolio.profit_loss += (holding.current_price - holding.buy_average) * holding.quantity
        portfolio.yield_on_cost += (holding.current_price - holding.buy_average) / holding.buy_average * 100
        portfolio.average_dividend_yield += holding.dividend_income / len(holdings)
        portfolio.weighted_average_price_to_book += price_to_book * holding.quantity
        portfolio.weighted_average_price_to_sales += price_to_sales * holding.quantity
        portfolio.weighted_average_enterprise_to_revenue += enterprise_to_revenue * holding.quantity
        portfolio.weighted_average_target_price += target_price * holding.quantity
        portfolio.beta += beta * holding.quantity
        portfolio.weighted_average_beta += beta * holding.quantity
        portfolio.trailing_pe += trailing_pe * holding.quantity
        portfolio.forward_pe += forward_pe * holding.quantity
        portfolio.alpha = 0
        portfolio.standard_deviation += calculate_standard_deviation(investment_trend) * holding.quantity
        portfolio.max_drawdown += calculate_max_drawdown(investment_trend) * holding.quantity
        portfolio.annualized_volatility = 0
        portfolio.tracking_error = 0

    return portfolio
