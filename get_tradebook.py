import pandas as pd
import os
from typing import List, Dict
from collections import defaultdict as defaultDict

from models.trade import Trade
from models.stock_info import StockInfo

def get_manual_trades(data_folder) -> List[Trade]:
    other_trades_df = pd.read_csv(f"{data_folder}/manual_trades.csv")
    other_trades_df['symbol'] = other_trades_df['symbol'].str.split('-').str[0]     # Normalize symbols

    other_trades = []
    for trade in other_trades_df.iterrows():
        other_trades.append(Trade(
            symbol = trade[1]['symbol'],
            quantity = abs(trade[1]['quantity']),
            price = trade[1]['price'],
            typ = 'buy' if trade[1]['quantity'] > 0 else 'sell',
            date = trade[1]['trade_date']
        ))
    return other_trades

def get_tradebook(data_folder) -> List[Trade]:
    tradebook_files = [
        os.path.join(data_folder, f) for f in os.listdir(data_folder)
        if f.startswith("tradebook") and f.endswith(".csv")
    ]
    fiscal_year_trades = [pd.read_csv(file) for file in tradebook_files]    # Read all tradebook files for individual fiscal year
    tradebook_df = pd.concat(fiscal_year_trades, ignore_index=True)    # Combine all tradebook files
    tradebook_df = tradebook_df.sort_values(by="order_execution_time")    # Sort by order execution time
    tradebook_df['symbol'] = tradebook_df['symbol'].str.split('-').str[0]     # Normalize symbols

    tradebook = []
    for trade in tradebook_df.iterrows():
        tradebook.append(Trade(
            symbol = trade[1]['symbol'],
            quantity = trade[1]['quantity'],
            price = trade[1]['price'],
            typ = trade[1]['trade_type'],
            date = trade[1]['trade_date']
        ))

    other_trades = get_manual_trades(data_folder)
    tradebook.extend(other_trades)
    tradebook.sort(key=lambda t: t.date)
    return tradebook

def get_adjusted_tradebook(tradebook: List[Trade], stock_info_store: Dict[str, StockInfo]) -> List[Trade]:
    tradebook_copy = tradebook.copy()
    for stock in stock_info_store.values():
        for split in stock.stock_splits:
            tradebook_copy.append(Trade(symbol = stock.symbol, quantity = 0, price = split.ratio, typ = 'split', date = split.split_date))
    
    tradebook_copy.sort(key=lambda t: t.date)

    adjusted_tradebook = []
    holdings = defaultDict(int)  # Track current holdings for each symbol

    for trade in tradebook_copy:
        if trade.typ == 'buy':
            holdings[trade.symbol] += trade.quantity
            adjusted_tradebook.append(trade)
        
        elif trade.typ == 'sell':
            holdings[trade.symbol] -= trade.quantity
            adjusted_tradebook.append(trade)
        
        elif trade.typ == 'split':
            if holdings[trade.symbol] > 0:
                bonus_quantity = holdings[trade.symbol] * (trade.price - 1)     # Split ratio - 1
                holdings[trade.symbol] += bonus_quantity
                adjusted_tradebook.append(Trade(symbol = trade.symbol, quantity = bonus_quantity, price = 0, typ = 'buy', date = trade.date))

    return adjusted_tradebook