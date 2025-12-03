import pytest
from click.testing import CliRunner
from ...main import cli

def test_add_bookmaker():
    runner = CliRunner()
    result = runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    assert result.exit_code == 0
    assert "Bookmaker 'TestBookmaker' added!" in result.output

def test_list_bookmakers():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    result = runner.invoke(cli, ['list-bookmakers'])
    assert result.exit_code == 0
    assert "TestBookmaker" in result.output

def test_add_bet():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    result = runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'Soccer', 'TestBookmaker'])
    assert result.exit_code == 0
    assert "Bet added" in result.output

def test_list_bets():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'Soccer', 'TestBookmaker'])
    result = runner.invoke(cli, ['list-bets'])
    assert result.exit_code == 0
    assert "Liverpool vs Chelsea" in result.output
    assert "Soccer" in result.output

def test_update_bet_result():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'Soccer', 'TestBookmaker'])
    result = runner.invoke(cli, ['update-bet-result', '1', 'won'])
    assert result.exit_code == 0
    assert "result updated to 'won'" in result.output

def test_delete_bet():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'Soccer', 'TestBookmaker'])
    result = runner.invoke(cli, ['delete-bet', '1'])
    assert result.exit_code == 0
    assert "Bet 1 deleted!" in result.output

def test_set_bankroll():
    runner = CliRunner()
    result = runner.invoke(cli, ['set-bankroll', '1000'])
    assert result.exit_code == 0
    assert "Bankroll set to $1000.00!" in result.output

def test_show_bankroll():
    runner = CliRunner()
    runner.invoke(cli, ['set-bankroll', '1000'])
    result = runner.invoke(cli, ['show-bankroll'])
    assert result.exit_code == 0
    assert "Current Balance" in result.output

def test_kelly_calculator():
    runner = CliRunner()
    result = runner.invoke(cli, ['kelly-calculator', '2.1', '60', '1000'])
    assert result.exit_code == 0
    assert "Full Kelly:" in result.output
    assert "Half Kelly:" in result.output
    assert "Quarter Kelly:" in result.output

def test_export_bets():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'Soccer', 'TestBookmaker'])
    result = runner.invoke(cli, ['export-bets', 'test_bets.csv'])
    assert result.exit_code == 0
    assert "Bets exported to test_bets.csv!" in result.output
