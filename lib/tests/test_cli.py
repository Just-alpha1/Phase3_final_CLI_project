import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from click.testing import CliRunner
from main import cli
from lib.db.session import init_db, get_db
from lib.db.models import Base
from sqlalchemy import create_engine

@pytest.fixture(scope="function", autouse=True)
def setup_database():

    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)

    import lib.db.session
    lib.db.session.engine = engine
    lib.db.session.SessionLocal = lib.db.session.sessionmaker(bind=engine)
    init_db()
    yield

    Base.metadata.drop_all(bind=engine)

def test_add_bookmaker():
    runner = CliRunner()
    result = runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    assert result.exit_code  == 0
    assert "Bookmaker 'TestBookmaker' added!" in result.output

def test_list_bookmakers():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    result = runner.invoke(cli, ['list-bookmakers'])
    assert result.exit_code  == 0
    assert "TestBookmaker" in result.output

def test_add_bet():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    result = runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'TestBookmaker'])
    assert result.exit_code  == 0
    assert "Bet placed" in result.output

def test_list_bets():
    runner = CliRunner()
    runner.invoke(cli, ['add-bookmaker', 'TestBookmaker'])
    runner.invoke(cli, ['add-bet', 'Liverpool vs Chelsea', 'Liverpool', '2.1', '100', 'TestBookmaker'])
    result = runner.invoke(cli, ['list-bets'])
    assert result.exit_code  == 0
    assert "Liverpool vs Chelsea" in result.output

def test_update_bet_result():
    runner = CliRunner()
