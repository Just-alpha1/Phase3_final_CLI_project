import pytest
from lib.db.session import init_db, get_db
from lib.db.models import Bookmaker, Bet

init_db()

def test_database_initialization():
    db = next(get_db())
    assert db is not None
    db.close()

def test_bookmaker_model():
    bookmaker = Bookmaker(name="Test Bookmaker")
    assert bookmaker.name  =="Test Bookmaker"
    assert bookmaker.id is None

def test_bet_model():
    bookmaker = Bookmaker(name="Test Bookmaker")
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, stake=100.0, sport="Soccer", bookmaker=bookmaker)
    assert bet.event  =="Test Event"
    assert bet.selection  =="Test Selection"
    assert bet.odds  ==2.0
    assert bet.stake  ==100.0
    assert bet.sport  =="Soccer"
    assert bet.result  =="pending"

def test_bet_profit_loss_calculation():
    bookmaker = Bookmaker(name="Test Bookmaker")
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, stake=100.0, sport="Soccer", bookmaker=bookmaker)

    assert bet.profit_loss()  ==0.0

    bet.result = "won"
    assert bet.profit_loss()  ==100.0

    bet.result = "lost"
    assert bet.profit_loss()  ==-100.0

    bet.result = "push"
    assert bet.profit_loss()  ==0.0

    bet.result = "void"
    assert bet.profit_loss()  ==0.0

def test_imports():
    try:
        from main import cli
        from lib.db.models import Base, Bookmaker, Bet, Bankroll, BankrollSnapshot
        from lib.db.session import get_db, init_db
        from lib.db.utils import get_current_bankroll, create_snapshot
        assert True
    except ImportError:
        assert False, "Import failed"