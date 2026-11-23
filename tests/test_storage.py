from expense_tracker.models import Expense
from expense_tracker.storage import load, save


def test_save_and_load(tmp_path):
    path = tmp_path / "data.json"
    save([Expense("Coffee", 1500, "food")], path)
    loaded = load(path)
    assert loaded[0].title == "Coffee"
