from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "data" / "db" / "app.sqlite3"

DATABASE_URL = f"sqlite:///{DB_PATH}"

print("DATABASE_URL =", DATABASE_URL)
print("DB_PATH =", DB_PATH)
class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)