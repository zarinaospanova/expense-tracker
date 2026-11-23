"""Business logic: totals, conversion and parsing."""
import math

from .models import Expense

# Single source of truth for exchange rates (1 unit -> KZT).
RATES_TO_KZT = {
    "KZT": 1,
    "USD": 480,
    "EUR": 520,
    "RUB": 5,
}


def parse_amount(text):
    """Parse a positive amount; "1500+300" style sums are allowed.

    Only plain numbers joined by "+" are accepted. Nothing is executed.
    """
    try:
        parts = [float(part) for part in str(text).split("+")]
    except ValueError:
        raise ValueError(f"Invalid amount: {text!r}") from None
    if any(not math.isfinite(p) or p < 0 for p in parts):
        raise ValueError(f"Invalid amount: {text!r}")
    amount = sum(parts)
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return amount


def convert_to_kzt(amount, currency):
    try:
        return amount * RATES_TO_KZT[currency]
    except KeyError:
        raise ValueError("Unknown currency: " + str(currency)) from None


def total(expenses):
    return sum(convert_to_kzt(e.amount, e.currency) for e in expenses)


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        value = convert_to_kzt(e.amount, e.currency)
        totals[e.category] = totals.get(e.category, 0) + value
    return totals


def add_expense(expenses, title, amount, category, currency="KZT"):
    expense = Expense(title, amount, category, currency)
    expenses.append(expense)
    return expense
