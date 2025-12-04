from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bookmaker(Base):
    __tablename__ = "bookmakers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    bets = relationship("Bet", back_populates="bookmaker", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bookmaker(name='{self.name}')>"

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True)
    event = Column(String(200), nullable=False)
    selection = Column(String(200), nullable=False)
    odds = Column(Float, nullable=False)
    stake = Column(Float, nullable=False)
    sport = Column(String(100), nullable=False)
    result = Column(String(20), default="pending")
    date_placed = Column(DateTime, default=datetime.utcnow)
    bookmaker_id = Column(Integer, ForeignKey("bookmakers.id"))
    bookmaker = relationship("Bookmaker", back_populates="bets")
    snapshots = relationship("BankrollSnapshot", back_populates="bet", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'result' not in kwargs:
            self.result = "pending"

    def profit_loss(self):
        if self.result == "won":
            profit = self.stake * (self.odds - 1)
            return round(profit, 2)
        elif self.result == "lost":
            loss = -self.stake
            return round(loss, 2)
        elif self.result in ("void", "push"):
            return 0.0
        else:
            return 0.0

    def __repr__(self):
        return f"<Bet(id={self.id}, event='{self.event}', selection='{self.selection}', result='{self.result}')>"

class Bankroll(Base):
    __tablename__ = "bankroll"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Bankroll(balance={self.balance:.2f})>"

class BankrollSnapshot(Base):
    __tablename__ = "bankroll_snapshots"

    id = Column(Integer, primary_key=True)
    balance = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    bet_id = Column(Integer, ForeignKey("bets.id"))
    bet = relationship("Bet", back_populates="snapshots")

    def __repr__(self):
        return f"<BankrollSnapshot(balance={self.balance:.2f}, timestamp='{self.timestamp}')>"