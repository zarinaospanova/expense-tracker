"""Command line interface."""
import argparse
import sys

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
    if args.command is None:
        parser.print_help()
        return 0

    try:
        expenses = storage.load(DATA_FILE)
    except storage.StorageError as exc:
        print("Error:", exc, file=sys.stderr)
        return 1

    if args.command == "add":
        try:
            amount = calculator.parse_amount(args.amount)
            calculator.convert_to_kzt(amount, args.currency)
        except ValueError as exc:
            print("Error:", exc, file=sys.stderr)
            return 2
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
    return 0
