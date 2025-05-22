import datetime
import os

from sqlalchemy import create_engine, Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user.pass@db:5432/urls")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(10), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    clicks = Column(Integer, default=0)


def init_db():
    Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
