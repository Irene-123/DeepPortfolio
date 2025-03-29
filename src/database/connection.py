import datetime
import sqlite3
from typing import List

DATE_TODAY = datetime.datetime.now().date().strftime("%Y-%m-%d")

def connect() -> List:
    """
    Connect to the SQLite database.
    Returns:
        connection: sqlite3.Connection
        cursor: sqlite3.Cursor
    """
    try:
        connection = sqlite3.connect(f"metadata/trading_agent_{DATE_TODAY}.db", autocommit=True)
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error as e:
        exit(f"Error connecting to the database: {e}")