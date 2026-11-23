from dataclasses import dataclass


@dataclass
class Expense:
    title: str
    amount: float
    category: str
    currency: str = "KZT"
