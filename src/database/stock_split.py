import sqlite3
import datetime
from typing import List

from .connection import connect
from src.models.stock_info import StockSplit

def create_stock_split_table():
    """
    Create the StockSplit table in the database.
    StockSplit table stores the data for stock splits.
    Returns:
        bool: True if the table was created successfully, False otherwise.
    """
    try:
        connection, cursor = connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS StockSplit (
                symbol TEXT,
                split_date DATE,
                ratio REAL,
                PRIMARY KEY (symbol, split_date)
            )
        """)
        return True
    except sqlite3.Error as e:
        exit(f"Error creating StockSplit table: {e}")
    finally:
        connection.close()

def insert_stock_split_into_db(symbol: str, split_date: datetime.date, ratio: float) -> bool:
    """
    Insert a stock split into the database.
    Args:
        symbol (str): NSE symbol for the stock.
        split_date (datetime.date): Date of the stock split.
        ratio (float): Ratio of the stock split.
    Returns:
        bool: True if the stock split was inserted successfully, False otherwise.
    """
    try:
        connection, cursor = connect()
        split_date_str = datetime.datetime.strftime(split_date, "%Y-%m-%d")
        cursor.execute("INSERT INTO StockSplit (symbol, split_date, ratio) VALUES (?, ?, ?)", (symbol, split_date_str, ratio))
        return True
    except sqlite3.Error as e:
        exit(f"Error inserting stock split into database: {e}")
    finally:
        connection.close()

def get_stock_splits_from_db(symbol: str) -> List[StockSplit]:
    """
    Get all stock splits for a given stock symbol from the database.
    Args:
        symbol (str): NSE symbol for the stock.
    Returns:
        List[StockSplit]: List of StockSplit objects for the given stock symbol.
    """
    try:
        connection, cursor = connect()
        cursor.execute("SELECT split_date, ratio FROM StockSplit WHERE symbol = ?", (symbol,))
        rows = cursor.fetchall()
        stock_splits = [StockSplit(split_date=row[0], ratio=row[1]) for row in rows]
        return stock_splits
    except sqlite3.Error as e:
        exit(f"Error fetching stock splits from database: {e}")
    finally:
        connection.close()
