from .models import BankrollSnapshot
from .session import get_db

def get_current_bankroll(db):
    # Get the most recent snapshot by ordering by ID descending
    latest_snapshot = db.query(BankrollSnapshot).order_by(BankrollSnapshot.id.desc()).first()
    
    if latest_snapshot:
        return latest_snapshot.balance
    else:
        return 0.0  # Starting balance when no history exists

def create_snapshot(db, balance):
    new_snapshot = BankrollSnapshot(balance=balance)
    db.add(new_snapshot)
    db.commit()

def get_latest_balance():
    db = next(get_db())
    try:
        current_balance = get_current_bankroll(db)
        return current_balance
    finally:
        db.close()