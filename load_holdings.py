import csv
from typing import Dict, List

from models.trade import Trade
from models.holding import Holding

def generate_holdings_from_tradebook(tradebook: list[Trade]) -> List[Holding]:
    """Generate holdings from tradebook."""
    holdings = {}
    for trade in tradebook:
        if trade.symbol in holdings.keys():
            if trade.typ == 'buy':
                total_quantity = holdings[trade.symbol].quantity + trade.quantity
                total_investment = holdings[trade.symbol].investment + (trade.quantity * trade.price)
                holdings[trade.symbol].quantity = total_quantity
                holdings[trade.symbol].investment = total_investment
            else:  # SELL
                holdings[trade.symbol].quantity -= trade.quantity
                holdings[trade.symbol].investment -= trade.quantity * holdings[trade.symbol].buy_average
            
            if holdings[trade.symbol].quantity == 0:
                del holdings[trade.symbol]
            else:
                holdings[trade.symbol].buy_average = holdings[trade.symbol].investment / holdings[trade.symbol].quantity
        else:
            holdings[trade.symbol] = Holding(
                symbol = trade.symbol,
                quantity = trade.quantity if trade.typ == 'buy' else -trade.quantity,
                buy_average = trade.price,
                investment = trade.quantity * trade.price
            )
    return list(holdings.values())