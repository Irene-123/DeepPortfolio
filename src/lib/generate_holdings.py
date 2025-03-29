import datetime
import pandas as pd
from typing import List, Dict

from src.models.trade import Trade
from src.models.holding import Holding
from src.models.stock_info import StockInfo

def calculate_index_revenue_for_holding(holding: Holding, index_data: pd.DataFrame):
    index_dict = {}
    for _, row in index_data.iterrows():
        index_dict[row["date"].strftime("%Y-%m-%d")] = [row["nifty50"], row["bsesensex"], row["niftybank"]]

    holding.risk_free_return_trend.append([holding.investment_trend[0][0], 0])
    holding.nifty50_return_trend.append([holding.investment_trend[0][0], 0])
    holding.bsesensex_return_trend.append([holding.investment_trend[0][0], 0])
    holding.niftybank_return_trend.append([holding.investment_trend[0][0], 0])

    for ind in range(1, len(holding.investment_trend)):
        last_date = holding.investment_trend[ind - 1][0]
        current_date = holding.investment_trend[ind][0]
        number_of_days = (holding.investment_trend[ind][0] - holding.investment_trend[ind - 1][0]).days
        
        holding.risk_free_return_trend.append([current_date, holding.investment_trend[ind - 1][1] * number_of_days * 0.075 / 365])
        holding.nifty50_return_trend.append([current_date, (index_dict[current_date][0] - index_dict[last_date][0]) * holding.investment_trend[ind - 1][1]])
        holding.bsesensex_return_trend.append([current_date, (index_dict[current_date][1] - index_dict[last_date][1]) * holding.investment_trend[ind - 1][1]])
        holding.niftybank_return_trend.append([current_date, (index_dict[current_date][2] - index_dict[last_date][2]) * holding.investment_trend[ind - 1][1]])

def generate_holdings_from_tradebook(symbols: List[str], tradebook: List[Trade], index_historical_data: pd.DataFrame, stock_info: Dict[str, StockInfo]) -> List[Holding]:
    holdings = {symbol: Holding(symbol=symbol) for symbol in symbols}
    for symbol in symbols:
        if symbol in stock_info.keys():
            holdings[symbol].stock_info = stock_info[symbol]

    for trade in tradebook:
        holdings[trade.symbol].trades.append(trade)

    for symbol in symbols:
        current_position = None
        for trade in holdings[symbol].trades:
            if current_position is None:
                current_position = trade.typ

            if trade.typ == current_position:
                if trade.typ == 'buy':
                    holdings[symbol].quantity += trade.quantity
                else:
                    holdings[symbol].quantity -= trade.quantity

                holdings[symbol].investment += trade.quantity * trade.price
            
            else:
                if trade.typ == 'buy':
                    holdings[symbol].realized_profit_history.append(min(trade.quantity, -holdings[symbol].quantity) * (holdings[symbol].buy_average - trade.price))
                    holdings[symbol].quantity -= trade.quantity
                else:
                    holdings[symbol].realized_profit_history.append(min(trade.quantity, holdings[symbol].quantity) * (trade.price - holdings[symbol].buy_average))
                    holdings[symbol].quantity += trade.quantity

                current_position = 'buy' if holdings[symbol].quantity > 0 else 'sell'
                holdings[symbol].realized_profit += holdings[symbol].realized_profit_history[-1]
                holdings[symbol].investment = abs(holdings[symbol].investment - trade.quantity * trade.price)

            holdings[symbol].quantity_trend.append([trade.date, holdings[symbol].quantity])
            holdings[symbol].buy_average = abs(holdings[symbol].investment / holdings[symbol].quantity) if holdings[symbol].quantity != 0 else 0
            holdings[symbol].investment_trend.append([trade.date, holdings[symbol].investment])

        holdings[symbol].current_price = stock_info[symbol].previous_close
        if current_position == 'buy' and holdings[symbol].quantity != 0:
            holdings[symbol].unrealized_profit = (holdings[symbol].current_price - holdings[symbol].buy_average) * holdings[symbol].quantity
        elif current_position == 'sell' and holdings[symbol].quantity != 0:
            holdings[symbol].unrealized_profit = (holdings[symbol].buy_average - holdings[symbol].current_price) * holdings[symbol].quantity
    
        calculate_index_revenue_for_holding(holdings[symbol], index_historical_data)
    return list(holdings.values())