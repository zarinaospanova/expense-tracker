# AGENTS.md — Expense Tracker

Instructions for AI coding agents (Claude, Copilot, Codex, etc.) working in this repository.
Read this file fully before making any change.

## 1. Purpose
A small command-line tool that records personal expenses in KZT, USD, EUR and RUB,
stores them in a local JSON file and prints totals in KZT. It is a course project:
correctness and safety matter more than features.

## 2. Architecture
| Path | Responsibility |
|---|---|
| `main.py` | Entry point, calls `expense_tracker.cli.main()` |
| `expense_tracker/cli.py` | argparse UI only (commands: `add`, `list`, `summary`) |
| `expense_tracker/calculator.py` | Business logic: parsing amounts, currency conversion, totals |
| `expense_tracker/storage.py` | Load/save expenses as JSON (`expenses.json`) |
| `expense_tracker/models.py` | `Expense` dataclass |
| `tests/` | pytest tests (one file per module) |

Rule: UI code stays in `cli.py`; calculations stay in `calculator.py`; file I/O stays in `storage.py`.

## 3. Setup
```
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
Requires Python 3.10 or newer. No network access is needed after installation.

## 4. Safe commands (allowed without asking)
```
python -m pytest -v                      # run all tests
python -m flake8 . --exclude=.venv      # lint
python -m py_compile main.py expense_tracker/*.py   # syntax/build check
git status / git diff / git log --oneline
```
When testing the CLI by hand, run it from a temporary folder (for example `cd "$(mktemp -d)"`)
so the real `expenses.json` is never touched.

## 5. Coding conventions
- PEP 8, max line length 79 (flake8 defaults). Lint must be clean.
- Small functions with clear names; no new global state.
- Currency rates live in ONE place (`RATES_TO_KZT` in `calculator.py`).
- Never use `eval`, `exec` or `pickle` on user input.
- Validate user input at the boundary and raise `ValueError` with a clear message.

## 6. Test expectations
- Every behavior change needs a test in `tests/`. Bug fixes need a test that failed before the fix.
- All tests and flake8 must pass before a change is proposed for review.
- Tests must not write outside pytest's `tmp_path`.
- Never delete, skip or weaken an existing test to make the suite pass.

## 7. Forbidden actions (never do these)
- Do not add, print, commit or request secrets, tokens, passwords or real personal data.
- Do not deploy, publish, push to `main` or create releases. Work on a separate branch only.
- Do not run destructive commands: `rm -rf`, `git reset --hard`, `git push --force`,
  `git clean -fd`, or deleting/overwriting `expenses.json`.
- Do not add, remove or upgrade dependencies in `requirements.txt` without human approval.
- Do not modify `AGENTS.md`, `.gitignore` or CI settings unless the task explicitly says so.
- Do not run commands that need the network other than `pip install -r requirements.txt`.

## 8. Review gates
1. Agent shows the full diff and the output of pytest and flake8.
2. A human (the repository owner, Zarina Ospanova) reviews every line of the diff.
3. Only the human commits/merges. Risky changes (storage format, input parsing) need a new test.

## 9. If something is unclear
Stop and ask the human instead of guessing. Report facts you checked separately from assumptions.
