import pytest
from lib.db.session import init_db, get_db
from lib.db.models import Bookmaker, Bet

# Initialize database for testing
init_db()

def test_database_initialization():
    """Test that database initializes correctly"""
    db = next(get_db())
    assert db is not None
    db.close()

def test_bookmaker_model():
    """Test Bookmaker model creation"""
    bookmaker = Bookmaker(name="Test Bookmaker")
    assert bookmaker.name == "Test Bookmaker"
    assert bookmaker.id is None  # Not committed yet

def test_bet_model():
    """Test Bet model creation"""
    bookmaker = Bookmaker(name="Test Bookmaker")
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, stake=100.0, sport="Soccer", bookmaker=bookmaker)
    assert bet.event == "Test Event"
    assert bet.selection == "Test Selection"
    assert bet.odds == 2.0
    assert bet.stake == 100.0
    assert bet.sport == "Soccer"
    assert bet.result == "pending"

def test_bet_profit_loss_calculation():
    """Test profit/loss calculation for bets"""
    bookmaker = Bookmaker(name="Test Bookmaker")
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, stake=100.0, sport="Soccer", bookmaker=bookmaker)

    # Test pending bet
    assert bet.profit_loss() == 0.0

    # Test won bet
    bet.result = "won"
    assert bet.profit_loss() == 100.0  # (2.0 - 1) * 100

    # Test lost bet
    bet.result = "lost"
    assert bet.profit_loss() == -100.0

    # Test push bet
    bet.result = "push"
    assert bet.profit_loss() == 0.0

    # Test void bet
    bet.result = "void"
    assert bet.profit_loss() == 0.0

def test_imports():
    """Test that all necessary modules can be imported"""
    try:
        from main import cli
        from lib.db.models import Base, Bookmaker, Bet, Bankroll, BankrollSnapshot
        from lib.db.session import get_db, init_db
        from lib.db.utils import get_current_bankroll, create_snapshot
        assert True
    except ImportError:
        assert False, "Import failed"
