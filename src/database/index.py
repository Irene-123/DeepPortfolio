import sqlite3
import pandas as pd
from .connection import connect

def create_index_table():
    """
    Create the IndexData table in the database.
    IndexData table stores the data for market indices like Nifty50, BSE Sensex, and Nifty Bank.
    Returns:
        bool: True if the table was created successfully, False otherwise.
    """
    try:
        connection, cursor = connect()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS IndexData (
                date DATE PRIMARY KEY,
                nifty50 REAL,
                bsesensex REAL,
                niftybank REAL
            )
        """)
        return True
    except sqlite3.Error as e:
        exit(f"Error creating IndexData table: {e}")
    finally:
        connection.close()

def insert_index_into_db(index_data: pd.DataFrame) -> bool:
    """
    Insert index data into the IndexData table in the database.
    Args:
        index_data (pd.DataFrame): DataFrame containing index data with columns - date, nifty50, bsesensex, niftybank.
    Returns:
        bool: True if the data was inserted successfully, False otherwise.
    """
    try:
        connection, cursor = connect()
        for _, row in index_data.iterrows():
            cursor.execute("""
                INSERT OR REPLACE INTO IndexData (
                    date, nifty50, bsesensex, niftybank
                ) VALUES (?, ?, ?, ?)
            """, (row['date'], row['nifty50'], row['bsesensex'], row['niftybank']))
        return True
    except sqlite3.Error as e:
        exit(f"Error inserting index data into database: {e}")
    finally:
        connection.close()

def get_index_from_db() -> pd.DataFrame:
    """
    Fetch all index data from the IndexData table in the database.
    Returns:
        pd.DataFrame: DataFrame containing all index data with columns - date, nifty50, bsesensex, niftybank.
    """
    try:
        connection, cursor = connect()
        cursor.execute("SELECT * FROM IndexData")
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        index_data = pd.DataFrame(rows, columns=columns)
        index_data['date'] = pd.to_datetime(index_data['date'])
        index_data['date'] = index_data['date'].dt.date
        return index_data
    except sqlite3.Error as e:
        exit(f"Error fetching index data from database: {e}")
    finally:
        connection.close()
