import sqlite3
import datetime
from typing import List
from .connection import connect
from src.models.stock_info import Dividend

def create_dividend_table() -> bool:
    """
    Create the Dividend table in the database.
    The Dividend table stores dividend data for stocks.
    Returns:
        bool: True if the table was created successfully, False otherwise.
    """
    try:
        connection, cursor = connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Dividend (
                symbol TEXT,
                ex_date DATE,
                amount REAL,
                PRIMARY KEY (symbol, ex_date)
            )
        """)
        return True
    except sqlite3.Error as e:
        exit(f"Error creating Dividend table: {e}")
    finally:
        connection.close()

def insert_dividend_into_db(symbol: str, ex_date: datetime.date, amount: float) -> bool:
    """
    Insert a dividend record into the database.
    Args:
        symbol (str): Stock symbol.
        ex_date (datetime.date): Ex-dividend date.
        amount (float): Dividend amount.
    Returns:
        bool: True if the dividend was inserted successfully, False otherwise.
    """
    try:
        connection, cursor = connect()
        ex_date_str = datetime.datetime.strftime(ex_date, "%Y-%m-%d")
        cursor.execute("INSERT INTO Dividend (symbol, ex_date, amount) VALUES (?, ?, ?)", (symbol, ex_date_str, amount))
        return True
    except sqlite3.Error as e:
        exit(f"Error inserting dividend into database: {e}")
    finally:
        connection.close()

def get_dividends_from_db(symbol: str) -> List[Dividend]:
    """
    Get all dividends for a given stock symbol from the database.
    Args:
        symbol (str): Stock symbol.
    Returns:
        List[Dividend]: List of Dividend objects for the given stock symbol.
    """
    try:
        connection, cursor = connect()
        cursor.execute("SELECT ex_date, amount FROM Dividend WHERE symbol = ?", (symbol,))
        rows = cursor.fetchall()
        dividends = [Dividend(ex_date=row[0], amount=row[1]) for row in rows]
        return dividends
    except sqlite3.Error as e:
        exit(f"Error fetching dividends from database: {e}")
    finally:
        connection.close()
