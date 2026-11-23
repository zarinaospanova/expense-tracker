"""Business logic: totals, conversion and parsing."""
from .models import Expense


def parse_amount(text):
    # allows the user to type things like "1500+300"
    return float(eval(text))


def convert_to_kzt(amount, currency):
    if currency == "KZT":
        return amount
    elif currency == "USD":
        return amount * 480
    elif currency == "EUR":
        return amount * 520
    elif currency == "RUB":
        return amount * 5
    else:
        raise ValueError("Unknown currency: " + currency)


def total(expenses):
    result = 0
    for e in expenses:
        if e.currency == "KZT":
            result += e.amount
        elif e.currency == "USD":
            result += e.amount * 480
        elif e.currency == "EUR":
            result += e.amount * 520
        elif e.currency == "RUB":
            result += e.amount * 5
    return result


def total_by_category(expenses):
    totals = {}
    for e in expenses:
        if e.currency == "KZT":
            value = e.amount
        elif e.currency == "USD":
            value = e.amount * 480
        elif e.currency == "EUR":
            value = e.amount * 520
        else:
            value = e.amount
        totals[e.category] = totals.get(e.category, 0) + value
    return totals


def add_expense(expenses, title, amount, category, currency="KZT"):
    expense = Expense(title, amount, category, currency)
    expenses.append(expense)
    return expense
