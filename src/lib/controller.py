import json

from src.lib.get_tradebook import generate_adjusted_tradebook, load_tradebook
from src.lib.get_stock_info import get_stock_info_store, get_index_data
from src.lib.generate_holdings import generate_holdings_from_tradebook
from src.lib.portfolio_parameters import portfolio_parameters
from src.models.portfolio import Portfolio

class Controller:
    def __init__(self):
        user_data = json.loads(open("user_data/user_data.json").read())
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.tradebook_files = user_data["tradebook"]
        self.manual_trades_file = user_data["manual_tradebook"]
        
        self.tradebook = load_tradebook(self.tradebook_files, self.manual_trades_file)
        self.symbols = set(entry.symbol for entry in self.tradebook)
        self.stock_info_store = get_stock_info_store(self.symbols)
        self.adjusted_tradebook = generate_adjusted_tradebook(self.tradebook, self.stock_info_store)
        self.index_returns = get_index_data()
        self.holdings = generate_holdings_from_tradebook(self.symbols, self.adjusted_tradebook, self.index_returns, self.stock_info_store)
        
        # Separate holdings into current and past holdings
        self.current_holdings = [holding for holding in self.holdings if holding.quantity != 0]
        self.past_holdings = [holding for holding in self.holdings if len(holding.realized_profit_history) != 0]

        self.portfolio = portfolio_parameters(self.current_holdings, self.stock_info_store)