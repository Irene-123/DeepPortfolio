import sqlite3
from .connection import connect
from src.models.stock_info import StockInfo

def create_stock_info_table() -> bool:
    """
    Create the StockInfo table in the database.
    StockInfo table stores the data for individual stocks.
    Returns:
        bool: True if the table was created successfully, False otherwise.
    """
    try:
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
        return True
    except sqlite3.Error as e:
        exit(f"Error creating StockInfo table: {e}")
    finally:
        connection.close()

def insert_stock_info_into_db(stock_info: StockInfo) -> bool:
    """
    Insert a StockInfo object into the database.
    Args:
        stock_info (StockInfo): StockInfo object to insert into the database
    Returns:
        bool: True if the StockInfo object was inserted successfully, False otherwise.
    """
    try:
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
        return True
    except sqlite3.Error as e:
        exit(f"Error inserting stock info into database: {e}")
    finally:
        connection.close()

def get_stock_info_from_db(symbol: str) -> StockInfo:
    """
    Get a StockInfo object from the database.
    Args:
        symbol (str): Stock symbol to get from the database
    Returns:
        StockInfo: StockInfo object from the database
    """
    try:
        connection, cursor = connect()
        cursor.execute("SELECT * FROM StockInfo WHERE symbol = ?", (symbol,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            stock_info = StockInfo(**dict(zip(columns, row)))
            return stock_info
        return None
    except Exception as e:
        exit(f"Error getting stock info from database: {e}")
    finally:
        connection.close()
