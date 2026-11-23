"""Business logic: totals, conversion and parsing."""
from .models import Expense

# Single source of truth for exchange rates (1 unit -> KZT).
RATES_TO_KZT = {
    "KZT": 1,
    "USD": 480,
    "EUR": 520,
    "RUB": 5,
}


def parse_amount(text):
    # allows the user to type things like "1500+300"
    return float(eval(text))


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
