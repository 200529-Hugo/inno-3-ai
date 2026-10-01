import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wmo_audit.db")
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)


class Base(DeclarativeBase):
    pass


def init_database() -> None:
    from app.models.audit import AuditRecord  # noqa: F401
    from app.models.review import ReviewDecision  # noqa: F401

    Base.metadata.create_all(engine)
