from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


engine = create_engine("sqlite:///betcli.db", echo=False)  # Set echo=True for debugging SQL
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always close the session to prevent memory leaks
