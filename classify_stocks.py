import yfinance as yf

def get_market_cap_thresholds(stock_symbols: list) -> tuple:
    """
    Fetch market capitalization thresholds for large-cap, mid-cap, and small-cap stocks.

    Args:
        stock_symbols (list): List of stock symbols to fetch market cap data.

    Returns:
        tuple: (large_cap_threshold, mid_cap_threshold)
    """
    market_caps = []
    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        market_cap = stock.info.get("marketCap", 0)
        if market_cap:
            market_caps.append(market_cap)

    # Sort market caps in descending order
    market_caps.sort(reverse=True)

    # Determine thresholds based on SEBI classification
    large_cap_threshold = market_caps[99] if len(market_caps) > 100 else 0  # Top 100
    mid_cap_threshold = market_caps[249] if len(market_caps) > 250 else 0   # Top 250

    return large_cap_threshold, mid_cap_threshold

def classify_stock(market_cap: float, large_cap_threshold: float, mid_cap_threshold: float) -> str:
    """
    Classify a stock as Large-Cap, Mid-Cap, or Small-Cap based on market capitalization.

    Args:
        market_cap (float): Market capitalization of the stock.
        large_cap_threshold (float): Minimum market cap for large-cap stocks.
        mid_cap_threshold (float): Minimum market cap for mid-cap stocks.

    Returns:
        str: Classification of the stock ("Large-Cap", "Mid-Cap", "Small-Cap").
    """
    if market_cap >= large_cap_threshold:
        return "Large-Cap"
    elif market_cap >= mid_cap_threshold:
        return "Mid-Cap"
    else:
        return "Small-Cap"

# Example usage
stock_symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "BAJFINANCE.NS"]  # Add more symbols
large_cap_threshold, mid_cap_threshold = get_market_cap_thresholds(stock_symbols)

market_cap = 12000  # Example market cap in crores
classification = classify_stock(market_cap, large_cap_threshold, mid_cap_threshold)
print(f"The stock is classified as: {classification}")
