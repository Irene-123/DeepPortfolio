import os
import json
import datetime

from src.lib.get_tradebook import generate_adjusted_tradebook, load_tradebook
from src.lib.get_stock_info import get_stock_info_store

class Controller:
    def __init__(self):
        # user_data = json.loads(open("user_data/user_data.json").read())
        # self.name = user_data["name"]
        # self.email = user_data["email"]
        # self.tradebook_files = user_data["tradebook"]
        # self.manual_trades_file = user_data["manual_tradebook"]
        
        # self.tradebook = load_tradebook(self.tradebook_files, self.manual_trades_file)
        # self.symbols = set(entry.symbol for entry in self.tradebook)
        # self.stock_info_store = get_stock_info_store(self.symbols)
        # self.adjusted_tradebook = generate_adjusted_tradebook(self.tradebook, self.stock_info_store)clear
        
        self.adjusted_tradebook = generate_adjusted_tradebook([], [])