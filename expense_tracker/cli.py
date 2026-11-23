"""Command line interface."""
import argparse

from . import calculator, storage

DATA_FILE = "expenses.json"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Expense tracker")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add")
    add.add_argument("title")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--currency", default="KZT")

    sub.add_parser("list")
    sub.add_parser("summary")

    args = parser.parse_args(argv)
    expenses = storage.load(DATA_FILE)

    if args.command == "add":
        amount = calculator.parse_amount(args.amount)
        calculator.add_expense(expenses, args.title, amount,
                               args.category, args.currency)
        storage.save(expenses, DATA_FILE)
        print("Added:", args.title, amount, args.currency)
    elif args.command == "list":
        for e in expenses:
            print(f"{e.title:20} {e.amount:>10} {e.currency} [{e.category}]")
    elif args.command == "summary":
        print("Total (KZT):", calculator.total(expenses))
        for cat, value in calculator.total_by_category(expenses).items():
            print(f"  {cat}: {value}")
    else:
        parser.print_help()
