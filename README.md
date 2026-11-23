# Expense Tracker

A small command-line tool to track personal expenses in different currencies
(KZT, USD, EUR, RUB). Totals are shown in KZT.

## Requirements

Python 3.10 or newer.

## Setup

    python3 -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt  # pytest and flake8 (development tools)

The app itself uses only the Python standard library.

## Usage

    python main.py add "Coffee" 1500 food
    python main.py add "Book" 10 study --currency USD
    python main.py add "Lunch" "1500+300" food
    python main.py list
    python main.py summary

Data is stored in `expenses.json` in the current folder (created on the first
`add`; ignored by git). Amounts must be positive numbers; only `+` is allowed
between numbers. Unknown currencies are rejected.

## Checks

    python -m pytest -v
    python -m flake8 . --exclude=.venv

## For AI agents

See `AGENTS.md` for allowed commands, forbidden actions and review rules.
