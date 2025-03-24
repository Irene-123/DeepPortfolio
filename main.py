from database import setup_database
from get_tradebook import get_tradebook, get_adjusted_tradebook
from get_stock_info import get_stock_info_store, get_index_data
from load_holdings import generate_holdings_from_tradebook
from revenue_per_symbol import calculate_revenue_per_symbol, calculate_revenue_for_index
import csv

setup_database()
index_data = get_index_data()
tradebook = get_tradebook('data')
stocks = set(entry.symbol for entry in tradebook)
stock_info_store = get_stock_info_store(stocks)
adjusted_tradebook = get_adjusted_tradebook(tradebook, stock_info_store)

# Save adjusted_tradebook to a CSV file
with open('adjusted_tradebook.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Symbol', 'Quantity', 'Price', 'Type', 'DATE'])  # Adjust headers as per the structure of tradebook entries
    for entry in adjusted_tradebook:
        writer.writerow([entry.symbol, entry.quantity, entry.price, entry.typ, entry.date])  # Adjust attributes as per the structure of tradebook entries

holdings = generate_holdings_from_tradebook(adjusted_tradebook)

holdings.sort(key=lambda h: h.symbol)
# for holding in holdings:
#     print(holding)

# print('\n\n')
revenue_per_symbol = calculate_revenue_per_symbol(adjusted_tradebook, stock_info_store)
realized_profit = sum(revenue['realized_profit'] for revenue in revenue_per_symbol.values())
unrealized_profit = sum(revenue['unrealized_profit'] for revenue in revenue_per_symbol.values())
# for symbol, revenue in revenue_per_symbol.items():
#     print(symbol, revenue)

calculate_revenue_for_index(adjusted_tradebook, index_data)
print("Realized Profit:", realized_profit)
print("Unrealized Profit:", unrealized_profit)