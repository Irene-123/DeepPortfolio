from typing import List
from collections import defaultdict
import numpy as np

from models.holding import Holding
from models.stock_info import StockInfo
from models.portfolio import Portfolio

def calculate_metrics(historical_prices, portfolio_returns, benchmark_returns, risk_free_rate):
    # Calculate Sharpe Ratio
    excess_returns = portfolio_returns - risk_free_rate
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) if np.std(excess_returns) > 0 else 0

    # Calculate Sortino Ratio
    downside_returns = excess_returns[excess_returns < 0]
    sortino_ratio = np.mean(excess_returns) / np.std(downside_returns) if np.std(downside_returns) > 0 else 0

    # Calculate Alpha
    alpha = np.mean(portfolio_returns - (risk_free_rate + benchmark_returns))

    # Calculate Standard Deviation
    standard_deviation = np.std(portfolio_returns)

    # Calculate Max Drawdown
    cumulative_returns = np.cumprod(1 + portfolio_returns)
    drawdowns = cumulative_returns / np.maximum.accumulate(cumulative_returns) - 1
    max_drawdown = np.min(drawdowns)

    # Calculate Annualized Volatility
    annualized_volatility = standard_deviation * np.sqrt(252)

    # Calculate Tracking Error
    tracking_error = np.std(portfolio_returns - benchmark_returns)

    # Calculate Annualized Return
    annualized_return = (1 + np.mean(portfolio_returns)) ** 252 - 1

    # Calculate Information Ratio
    information_ratio = (np.mean(portfolio_returns - benchmark_returns) / tracking_error) if tracking_error > 0 else 0

    # Placeholder for Turnover Ratio (requires transaction data)
    turnover_ratio = 0

    # Placeholder for Concentration Ratio (requires weights of largest holdings)
    concentration_ratio = 0

    return sharpe_ratio, sortino_ratio, alpha, standard_deviation, max_drawdown, annualized_volatility, tracking_error, annualized_return, information_ratio, turnover_ratio, concentration_ratio

def generate_portfolio(stocks: List[StockInfo], holdings: List[Holding], historical_prices, portfolio_returns, benchmark_returns, risk_free_rate) -> Portfolio:
    total_investment = sum(holding.investment for holding in holdings)
    current_value = sum(holding.quantity * stock.previous_close for stock, holding in zip(stocks, holdings))
    profit_loss = current_value - total_investment
    yield_on_cost = (current_value / total_investment) - 1 if total_investment > 0 else 0
    stock_weights = [holding.investment / total_investment for holding in holdings]

    sector_weights = defaultdict(lambda: {"count": 0, "weight": 0})
    for stock, weight in zip(stocks, stock_weights):
        sector_weights[stock.sector]["count"] += 1
        sector_weights[stock.sector]["weight"] += weight

    industry_weights = defaultdict(lambda: {"count": 0, "weight": 0})
    for stock, weight in zip(stocks, stock_weights):
        industry_weights[stock.industry]["count"] += 1
        industry_weights[stock.industry]["weight"] += weight

    portfolio_beta = sum(stock.beta * weight for stock, weight in zip(stocks, stock_weights))
    portfolio_dividend_yield = sum(stock.dividend_yield * weight for stock, weight in zip(stocks, stock_weights))
    average_dividend_yield = sum(stock.five_year_average_dividend_yield * weight for stock, weight in zip(stocks, stock_weights))
    trailing_pe = sum(stock.trailing_pe * weight for stock, weight in zip(stocks, stock_weights))
    forward_pe = sum(stock.forward_pe * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_price_to_book = sum(stock.price_to_book * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_price_to_sales = sum(stock.price_to_sales * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_enterprise_to_revenue = sum(stock.enterprise_to_revenue * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_enterprise_to_ebitda = sum(stock.enterprise_to_ebitda * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_target_price = sum(stock.target_price * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_market_cap = sum(stock.market_cap * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_ebitda_margin = sum(stock.ebitda_margin * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_operating_margin = sum(stock.operating_margin * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_gross_margin = sum(stock.gross_margin * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_revenue_growth = sum(stock.revenue_growth * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_eps_growth = sum(stock.eps_growth * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_earnings_growth = sum(stock.earnings_growth * weight for stock, weight in zip(stocks, stock_weights))
    weighted_average_debt_to_equity = sum(stock.debt_to_equity * weight for stock, weight in zip(stocks, stock_weights))

    sharpe_ratio, sortino_ratio, alpha, standard_deviation, max_drawdown, annualized_volatility, tracking_error, annualized_return, information_ratio, turnover_ratio, concentration_ratio = calculate_metrics(
        historical_prices, portfolio_returns, benchmark_returns, risk_free_rate
    )

    return Portfolio(
        stocks=stocks,
        holdings=holdings,
        total_investment=total_investment,
        current_value=current_value,
        profit_loss=profit_loss,
        yield_on_cost=yield_on_cost,
        dividend_yield=portfolio_dividend_yield,
        average_dividend_yield=average_dividend_yield,
        weighted_average_dividend_yield=portfolio_dividend_yield,
        trailing_pe=trailing_pe,
        forward_pe=forward_pe,
        weighted_average_price_to_book=weighted_average_price_to_book,
        weighted_average_price_to_sales=weighted_average_price_to_sales,
        weighted_average_enterprise_to_revenue=weighted_average_enterprise_to_revenue,
        weighted_average_enterprise_to_ebitda=weighted_average_enterprise_to_ebitda,
        weighted_average_target_price=weighted_average_target_price,
        beta=portfolio_beta,
        weighted_average_beta=portfolio_beta,
        sharpe_ratio=sharpe_ratio,
        sortino_ratio=sortino_ratio,
        alpha=alpha,
        standard_deviation=standard_deviation,
        max_drawdown=max_drawdown,
        annualized_volatility=annualized_volatility,
        tracking_error=tracking_error,
        annualized_return=annualized_return,
        information_ratio=information_ratio,
        turnover_ratio=turnover_ratio,
        sector_weights=dict(sector_weights),
        industry_weights=dict(industry_weights),
        concentration_ratio=concentration_ratio,
        weighted_average_market_cap=weighted_average_market_cap,
        weighted_average_ebitda_margin=weighted_average_ebitda_margin,
        weighted_average_operating_margin=weighted_average_operating_margin,
        weighted_average_gross_margin=weighted_average_gross_margin,
        weighted_average_revenue_growth=weighted_average_revenue_growth,
        weighted_average_eps_growth=weighted_average_eps_growth,
        weighted_average_earnings_growth=weighted_average_earnings_growth,
        weighted_average_debt_to_equity=weighted_average_debt_to_equity
    )
