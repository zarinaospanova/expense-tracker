from expense_tracker.calculator import (add_expense, convert_to_kzt,
                                        parse_amount, total,
                                        total_by_category)
from expense_tracker.models import Expense


def test_total_kzt_only():
    expenses = [Expense("Coffee", 1500, "food"), Expense("Bus", 200, "transport")]
    assert total(expenses) == 1700


def test_total_mixed_currency():
    expenses = [Expense("Book", 10, "study", "USD"), Expense("Taxi", 1000, "transport")]
    assert total(expenses) == 5800


def test_total_by_category():
    expenses = [Expense("Coffee", 1500, "food"), Expense("Lunch", 2500, "food")]
    assert total_by_category(expenses) == {"food": 4000}


def test_convert_usd():
    assert convert_to_kzt(2, "USD") == 960


def test_parse_amount():
    assert parse_amount("1500") == 1500.0


def test_add_expense():
    expenses = []
    add_expense(expenses, "Milk", 600, "food")
    assert len(expenses) == 1
