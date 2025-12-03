from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Bookmaker(Base):
    __tablename__ = "bookmakers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    # One-to-Many → many bets belong to one bookmaker
    bets = relationship("Bet", back_populates="bookmaker", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bookmaker {self.name}>"

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    event = Column(String(200), nullable=False)
    selection = Column(String(200), nullable=False)
    odds = Column(Float, nullable=False)          # decimal odds
    stake = Column(Float, nullable=False)
    sport = Column(String(100), nullable=False)   # sport category
    result = Column(String(20), default="pending")  # won, lost, push, void, pending
    date_placed = Column(DateTime, default=datetime.utcnow)

    # Foreign key to bookmaker
    bookmaker_id = Column(Integer, ForeignKey("bookmakers.id"))
    bookmaker = relationship("Bookmaker", back_populates="bets")

    # One-to-Many → one bet creates many bankroll snapshots
    snapshots = relationship("BankrollSnapshot", back_populates="bet", cascade="all, delete-orphan")

    def profit_loss(self):
        if self.result == "won":
            return round(self.stake * (self.odds - 1), 2)
        elif self.result == "lost":
            return round(-self.stake, 2)
        elif self.result == "void":
            return 0.0  # stake returned
        else:
            return 0.0

class Bankroll(Base):
    __tablename__ = "bankroll"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)

class BankrollSnapshot(Base):
    __tablename__ = "bankroll_snapshots"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    bet_id = Column(Integer, ForeignKey("bets.id"))
    bet = relationship("Bet", back_populates="snapshots")
