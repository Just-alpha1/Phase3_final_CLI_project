import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, Bookmaker, Bet, Bankroll, BankrollSnapshot
from lib.db.session import init_db, get_db

def test_bookmaker_creation():
    init_db()
    db = next(get_db())
    bookmaker = Bookmaker(name="Test Bookmaker")
    db.add(bookmaker)
    db.commit()
    assert bookmaker.id is not None
    assert bookmaker.name == "Test Bookmaker"

def test_bet_creation():
    db = next(get_db())
    bookmaker = Bookmaker(name="Test Bookmaker")
    db.add(bookmaker)
    db.commit()
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, actual_stake=100.0, bookmaker=bookmaker)
    db.add(bet)
    db.commit()
    assert bet.id is not None
    assert bet.event == "Test Event"
    assert bet.selection == "Test Selection"
    assert bet.odds == 2.0
    assert bet.actual_stake == 100.0
    assert bet.outcome == "pending"
    assert bet.bookmaker == bookmaker

def test_profit_loss_calculation():
    db = next(get_db())
    bookmaker = Bookmaker(name="Test Bookmaker")
    db.add(bookmaker)
    db.commit()
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, stake=100.0, sport="Soccer", bookmaker=bookmaker)
    db.add(bet)
    db.commit()

    bet.result = "won"
    assert bet.profit_loss() == 100.0

    bet.result = "lost"
    assert bet.profit_loss() == -100.0

    bet.result = "push"
    assert bet.profit_loss() == 0.0

    bet.result = "void"
    assert bet.profit_loss() == 0.0