from dataclasses import dataclass

@dataclass
class Holding:
    symbol: str
    quantity: int
    buy_average: float
    investment: float