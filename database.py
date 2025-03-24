import sqlite3
import pandas as pd
import datetime
from typing import List

from models.stock_info import StockInfo, StockSplit, Dividend

DATE_TODAY = datetime.datetime.now().date().strftime("%Y-%m-%d")

def connect():
    connection = sqlite3.connect(f"trading_agent_{DATE_TODAY}.db", autocommit=True)
    cursor = connection.cursor()
    return connection, cursor

# StockInfo table operations
# ==========================================================================================================================
def create_stock_info_table():
    connection, cursor = connect()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS StockInfo (
            symbol TEXT PRIMARY KEY,
            symbol_yf TEXT,
            name TEXT,
            city TEXT,
            industry TEXT,
            sector TEXT,
            previous_close REAL,
            volume INTEGER,
            average_volume_10days INTEGER,
            average_volume_3months INTEGER,
            fifty_two_week_low REAL,
            fifty_two_week_high REAL,
            fifty_two_week_change REAL,
            market_cap INTEGER,
            book_value REAL,
            price_to_sales_trailing_12_months REAL,
            price_to_book REAL,
            trailing_pe REAL,
            forward_pe REAL,
            trailing_eps REAL,
            forward_eps REAL,
            price_eps_current_year REAL,
            fifty_day_average REAL,
            two_hundred_day_average REAL,
            beta REAL,
            debt_to_equity REAL,
            enterprise_to_revenue REAL,
            enterprise_to_ebitda REAL,
            ebitda INTEGER,
            total_debt INTEGER,
            total_revenue INTEGER,
            revenue_per_share REAL,
            gross_profit INTEGER,
            revenue_growth REAL,
            gross_margins REAL,
            ebitda_margins REAL,
            operating_margins REAL,
            eps_trailing_12months REAL,
            eps_forward REAL,
            eps_current_year REAL,
            target_high_price REAL,
            target_low_price REAL,
            target_mean_price REAL,
            dividend_yield REAL,
            five_year_average_dividend_yield REAL
        )
    """)
    connection.close()

def insert_stock_info_into_db(stock_info: StockInfo):
    connection, cursor = connect()
    cursor.execute("""
        INSERT INTO StockInfo (
            symbol, symbol_yf, name, city, industry, sector, previous_close, volume, 
            average_volume_10days, average_volume_3months, fifty_two_week_low, 
            fifty_two_week_high, fifty_two_week_change, market_cap, book_value, 
            price_to_sales_trailing_12_months, price_to_book, trailing_pe, 
            forward_pe, trailing_eps, forward_eps, price_eps_current_year, 
            fifty_day_average, two_hundred_day_average, beta, debt_to_equity, 
            enterprise_to_revenue, enterprise_to_ebitda, ebitda, total_debt, 
            total_revenue, revenue_per_share, gross_profit, revenue_growth, 
            gross_margins, ebitda_margins, operating_margins, eps_trailing_12months, 
            eps_forward, eps_current_year, target_high_price, target_low_price, 
            target_mean_price, dividend_yield, five_year_average_dividend_yield
        ) VALUES (
            :symbol, :symbol_yf, :name, :city, :industry, :sector, :previous_close, :volume, 
            :average_volume_10days, :average_volume_3months, :fifty_two_week_low, 
            :fifty_two_week_high, :fifty_two_week_change, :market_cap, :book_value, 
            :price_to_sales_trailing_12_months, :price_to_book, :trailing_pe, 
            :forward_pe, :trailing_eps, :forward_eps, :price_eps_current_year, 
            :fifty_day_average, :two_hundred_day_average, :beta, :debt_to_equity, 
            :enterprise_to_revenue, :enterprise_to_ebitda, :ebitda, :total_debt, 
            :total_revenue, :revenue_per_share, :gross_profit, :revenue_growth, 
            :gross_margins, :ebitda_margins, :operating_margins, :eps_trailing_12months, 
            :eps_forward, :eps_current_year, :target_high_price, :target_low_price, 
            :target_mean_price, :dividend_yield, :five_year_average_dividend_yield
        )
    """, stock_info.__dict__)
    connection.close()

def get_stock_info_from_db(symbol: str) -> StockInfo:
    connection, cursor = connect()
    cursor.execute("SELECT * FROM StockInfo WHERE symbol = ?", (symbol,))
    row = cursor.fetchone()
    connection.close()
    if row:
        columns = [column[0] for column in cursor.description]
        stock_info = StockInfo(**dict(zip(columns, row)))
        return stock_info
    return None

# StockSplit table operations
# ==========================================================================================================================
def create_stock_split_table():
    connection, cursor = connect()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS StockSplit (
            symbol TEXT,
            split_date DATE,
            ratio REAL,
            PRIMARY KEY (symbol, split_date)
        )
    """)
    connection.close()

def insert_stock_split_into_db(symbol: str, split_date: datetime.date, ratio: float):
    connection, cursor = connect()
    split_date_str = datetime.datetime.strftime(split_date, "%Y-%m-%d")
    cursor.execute("INSERT INTO StockSplit (symbol, split_date, ratio) VALUES (?, ?, ?)", (symbol, split_date_str, ratio))
    connection.close()

def get_stock_splits_from_db(symbol: str) -> List[StockSplit]:
    connection, cursor = connect()
    cursor.execute("SELECT split_date, ratio FROM StockSplit WHERE symbol = ?", (symbol,))
    rows = cursor.fetchall()
    stock_splits = [StockSplit(split_date=row[0], ratio=row[1]) for row in rows]
    connection.close()
    return stock_splits

# Dividend table operations
# ==========================================================================================================================
def create_dividend_table():
    connection, cursor = connect()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Dividend (
            symbol TEXT,
            ex_date DATE,
            amount REAL,
            PRIMARY KEY (symbol, ex_date)
        )
    """)
    connection.close()

def insert_dividend_into_db(symbol: str, ex_date: datetime.date, amount: float):
    connection, cursor = connect()
    ex_date_str = datetime.datetime.strftime(ex_date, "%Y-%m-%d")
    cursor.execute("INSERT INTO Dividend (symbol, ex_date, amount) VALUES (?, ?, ?)", (symbol, ex_date_str, amount))
    connection.close()

def get_dividends_from_db(symbol: str) -> List[Dividend]:
    connection, cursor = connect()
    cursor.execute("SELECT ex_date, amount FROM Dividend WHERE symbol = ?", (symbol,))
    rows = cursor.fetchall()
    dividends = [Dividend(ex_date=row[0], amount=row[1]) for row in rows]
    connection.close()
    return dividends

# Index table operations
# ==========================================================================================================================
def create_index_table():
    connection, cursor = connect()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS IndexData (
            date DATE PRIMARY KEY,
            nifty50 REAL,
            bsesensex REAL,
            niftybank REAL
        )
    """)
    connection.close()

def insert_index_into_db(index_data: pd.DataFrame):
    connection, cursor = connect()
    # Insert each row into the Index table
    for _, row in index_data.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO IndexData (
                date, nifty50, bsesensex, niftybank
            ) VALUES (?, ?, ?, ?)
        """, (row['date'], row['nifty50'], row['bsesensex'], row['niftybank']))
    connection.close()

def get_index_from_db() -> pd.DataFrame:
    connection, cursor = connect()
    cursor.execute("SELECT * FROM IndexData")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    connection.close()
    index_data = pd.DataFrame(rows, columns=columns)
    index_data['date'] = pd.to_datetime(index_data['date'])
    index_data['date'] = index_data['date'].dt.date
    return index_data

# Database operations
# ==========================================================================================================================
def setup_database():
    create_stock_info_table()
    create_stock_split_table()
    create_dividend_table()
    create_index_table()
