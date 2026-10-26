import sys

import pytest

import main
from expense_manager import ExpenseManager


@pytest.fixture
def cli(tmp_path, monkeypatch, capsys):
    """Run main.main() with the given arguments against a temporary data file."""
    data_file = tmp_path / "expenses.json"
    monkeypatch.setattr(main, "ExpenseManager", lambda: ExpenseManager(str(data_file)))

    def run(*args):
        monkeypatch.setattr(sys, "argv", ["main.py", *args])
        main.main()
        return capsys.readouterr().out

    return run


def test_list_renders_a_rounded_table(cli):
    # Regression: main.py imports tabulate and uses tablefmt="rounded_grid" (tabulate >= 0.9.0),
    # so the CLI crashed in an environment installed from requirements.txt without tabulate.
    cli("add", "--amount", "14.50", "--cat", "Food", "--desc", "Lunch burrito", "--date", "2024-03-15")
    output = cli("list")
    assert "╭" in output and "Lunch burrito" in output
