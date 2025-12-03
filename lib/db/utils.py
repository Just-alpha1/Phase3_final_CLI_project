from .models import BankrollSnapshot
from .session import get_db

def get_current_bankroll(db):
    """Return the latest balance or 0.0 if no snapshots yet"""
    latest = db.query(BankrollSnapshot).order_by(BankrollSnapshot.id.desc()).first()
    return latest.balance if latest else 0.0

def create_snapshot(db, balance):
    """Create a new bankroll snapshot"""
    snapshot = BankrollSnapshot(balance=balance)
    db.add(snapshot)
    db.commit()