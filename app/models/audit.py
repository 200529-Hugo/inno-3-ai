from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditRecord(Base):
    __tablename__ = "audit_records"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    citizen_token: Mapped[str] = mapped_column(String, index=True)
    risk: Mapped[str] = mapped_column(String)
    risk_score: Mapped[float] = mapped_column(Float)
    flags: Mapped[dict] = mapped_column(JSON)
    proposal: Mapped[str] = mapped_column(String)
    rationale: Mapped[str] = mapped_column(String)
    route: Mapped[str] = mapped_column(String)
