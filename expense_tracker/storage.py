"""Save and load expenses as JSON."""
import json

from .models import Expense


def save(expenses, path):
    data = [e.__dict__ for e in expenses]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return [Expense(**item) for item in data]
