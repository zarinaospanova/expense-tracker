"""Save and load expenses as JSON."""
import json
import os
import tempfile

from .models import Expense


class StorageError(Exception):
    """Raised when the data file exists but cannot be read."""


def save(expenses, path):
    data = [e.__dict__ for e in expenses]
    folder = os.path.dirname(os.path.abspath(path))
    # Write to a temporary file first, then replace the real file in one
    # step, so a crash during writing cannot leave half-written JSON.
    fd, tmp_path = tempfile.mkstemp(dir=folder, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2,
                      allow_nan=False)
        os.replace(tmp_path, path)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def load(path):
    if not os.path.exists(path):
        return []  # first run: no data yet
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return [Expense(**item) for item in data]
    except (json.JSONDecodeError, TypeError) as exc:
        raise StorageError(
            f"Data file '{path}' is damaged and was not changed: {exc}"
        ) from None
