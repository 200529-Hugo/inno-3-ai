from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ReviewDecision(Base):
    __tablename__ = "review_decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    audit_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    decision: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(Text)
    reviewer_name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
