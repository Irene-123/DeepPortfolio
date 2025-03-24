from typing import List, Dict
import pandas as pd
from collections import defaultdict
from models.trade import Trade
from models.stock_info import StockInfo
from datetime import datetime

def calculate_revenue_per_symbol(tradebook: List[Trade], stock_info_store: Dict[str, StockInfo]):
    trades_by_symbol = defaultdict(list)
    for trade in tradebook:
        trades_by_symbol[trade.symbol].append(trade)

    revenue_per_symbol = {}
    for symbol, trades in trades_by_symbol.items():
        price_average = None
        quantity = None
        last_date = None
        risk_free_return = 0
        realized_profit = 0
        unrealized_profit = 0

        for trade in trades:
            if last_date is None:
                last_date = datetime.strptime(trade.date, "%Y-%m-%d")
                quantity = trade.quantity if trade.typ == 'buy' else -trade.quantity
                price_average = trade.price
                continue

            trade_date = datetime.strptime(trade.date, "%Y-%m-%d")
            duration = (trade_date - last_date).days
            risk_free_return += duration * price_average * quantity * 0.075

            if quantity > 0 and trade.typ == 'sell':
                realized_profit += trade.quantity * (trade.price - price_average)
                quantity -= trade.quantity
            elif quantity < 0 and trade.typ == 'buy':
                realized_profit += trade.quantity * (price_average - trade.price)
                quantity += trade.quantity
            elif quantity >= 0 and trade.typ == 'buy':
                price_average = (price_average * quantity + trade.price * trade.quantity) / (quantity + trade.quantity)
                quantity += trade.quantity
            elif quantity <= 0 and trade.typ == 'sell':
                price_average = (price_average * abs(quantity) + trade.price * trade.quantity) / (abs(quantity) + trade.quantity)
                quantity -= trade.quantity
            
            last_date = trade_date

        if quantity != 0:
            ltp = stock_info_store[symbol].previous_close
            unrealized_profit = quantity * (ltp - price_average)

        revenue_per_symbol[symbol] = {
            "risk_free_return": risk_free_return / 365,
            "realized_profit": realized_profit,
            "unrealized_profit": unrealized_profit
        }
    return revenue_per_symbol

def calculate_revenue_for_index(tradebook: List[Trade], index_data: pd.DataFrame):
    index_dict = {}
    for _, row in index_data.iterrows():
        index_dict[row["date"].strftime("%Y-%m-%d")] = [row["nifty50"], row["bsesensex"], row["niftybank"]]

    holdings = defaultdict(int)
    current_investment = 0
    index_returns = [0, 0, 0]
    last_date = None
    for trade in tradebook:
        if last_date is None:
            last_date = trade.date
            current_investment += trade.quantity * trade.price
            holdings[trade.symbol] += trade.quantity if trade.typ == 'buy' else -trade.quantity
            continue

        change_in_index = [(index_dict[trade.date][i] - index_dict[last_date][i])/index_dict[last_date][i] for i in range(3)]
        index_returns = [index_returns[i] + change_in_index[i] * current_investment for i in range(3)]
        if trade.typ == 'buy' and holdings[trade.symbol] >= 0:
            current_investment += trade.quantity * trade.price
            holdings[trade.symbol] += trade.quantity
        elif trade.typ == 'sell' and holdings[trade.symbol] <= 0:
            current_investment += trade.quantity * trade.price
            holdings[trade.symbol] -= trade.quantity
        elif trade.typ == 'buy' and holdings[trade.symbol] < 0:
            current_investment -= trade.quantity * trade.price
            holdings[trade.symbol] += trade.quantity
        elif trade.typ == 'sell' and holdings[trade.symbol] > 0:
            current_investment -= trade.quantity * trade.price
            holdings[trade.symbol] -= trade.quantity

        last_date = trade.date
    
    print("Index Returns: ", index_returns)
