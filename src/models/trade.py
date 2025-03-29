import datetime
from dataclasses import dataclass

@dataclass
class Trade:
    symbol: str
    quantity: int
    price: float
    typ: str
    date: datetime.datetime
    remarks: str = ""