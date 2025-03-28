from .dividend import create_dividend_table
from .index import create_index_table
from .stock_info import create_stock_info_table
from .stock_split import create_stock_split_table

create_stock_info_table()
create_stock_split_table()
create_dividend_table()
create_index_table()