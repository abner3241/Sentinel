import pytest
from click.testing import CliRunner
from core.cli import main

def test_cli_backtest_help():
    runner = CliRunner()
    result = runner.invoke(main, ["backtest", "--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
