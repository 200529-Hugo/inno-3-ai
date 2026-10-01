import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select

from app.database import SessionLocal
from app.models.audit import AuditRecord
from app.models.schemas import AuditIn


class AuditService:
    @staticmethod
    def create(audit: AuditIn) -> dict[str, Any]:
        record_id = str(uuid.uuid4())
        record = AuditRecord(
            id=record_id,
            created_at=datetime.now(timezone.utc),
            citizen_token=audit.citizenToken,
            risk=audit.risk,
            risk_score=audit.riskScore,
            flags=audit.flags,
            proposal=audit.proposal,
            rationale=audit.rationale,
            route=audit.route,
        )
        with SessionLocal() as session:
            session.add(record)
            session.commit()
        return {"logged": True, "auditId": record_id}

    @staticmethod
    def list_recent(limit: int = 100) -> list[dict[str, Any]]:
        query = select(AuditRecord).order_by(AuditRecord.created_at.desc()).limit(limit)
        with SessionLocal() as session:
            records = session.scalars(query).all()
            return [
                {
                    "id": record.id,
                    "createdAt": record.created_at,
                    "citizenToken": record.citizen_token,
                    "risk": record.risk,
                    "riskScore": record.risk_score,
                    "flags": record.flags,
                    "proposal": record.proposal,
                    "rationale": record.rationale,
                    "route": record.route,
                }
                for record in records
            ]
