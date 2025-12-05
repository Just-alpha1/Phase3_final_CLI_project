import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.db.models import Base, Bookmaker, Bet, Bankroll, BankrollSnapshot
from lib.db.session import init_db, get_db

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

def test_bookmaker_creation():
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
    bet = Bet(event="Test Event", selection="Test Selection", odds=2.0, actual_stake=100.0, bookmaker=bookmaker)
    db.add(bet)
    db.commit()

    bet.outcome = "won"
    assert bet.profit_loss() == 100.0

    bet.outcome = "lost"
    assert bet.profit_loss() == -100.0

    bet.outcome = "push"
    assert bet.profit_loss() == 0.0

    bet.outcome = "void"
    assert bet.profit_loss() == 0.0
