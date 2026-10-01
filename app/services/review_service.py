import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select

from app.database import SessionLocal
from app.models.audit import AuditRecord
from app.models.review import ReviewDecision
from app.models.schemas import ReviewDecisionIn


class ReviewService:
    @staticmethod
    def list_cases() -> list[dict[str, Any]]:
        audit_query = (
            select(AuditRecord)
            .where(AuditRecord.route == "human_review")
            .order_by(AuditRecord.created_at.desc())
            .limit(100)
        )
        with SessionLocal() as session:
            audits = session.scalars(audit_query).all()
            decisions = session.scalars(select(ReviewDecision)).all()
            decision_by_audit = {decision.audit_id: decision for decision in decisions}
            return [ReviewService._serialize_case(audit, decision_by_audit.get(audit.id)) for audit in audits]

    @staticmethod
    def decide(audit_id: str, request: ReviewDecisionIn) -> dict[str, Any] | None:
        with SessionLocal() as session:
            audit = session.get(AuditRecord, audit_id)
            if audit is None or audit.route != "human_review":
                return None

            decision = session.scalar(select(ReviewDecision).where(ReviewDecision.audit_id == audit_id))
            if decision is None:
                decision = ReviewDecision(id=str(uuid.uuid4()), audit_id=audit_id)
                session.add(decision)

            decision.decision = request.decision
            decision.notes = request.notes
            decision.reviewer_name = request.reviewerName
            decision.created_at = datetime.now(timezone.utc)
            session.commit()
            session.refresh(decision)
            return ReviewService._serialize_decision(decision)

    @staticmethod
    def _serialize_case(audit: AuditRecord, decision: ReviewDecision | None) -> dict[str, Any]:
        return {
            "auditId": audit.id,
            "createdAt": audit.created_at,
            "citizenToken": audit.citizen_token,
            "risk": audit.risk,
            "riskScore": audit.risk_score,
            "flags": audit.flags,
            "proposal": audit.proposal,
            "rationale": audit.rationale,
            "status": "afgerond" if decision else "open",
            "decision": ReviewService._serialize_decision(decision) if decision else None,
        }

    @staticmethod
    def _serialize_decision(decision: ReviewDecision) -> dict[str, Any]:
        return {
            "id": decision.id,
            "auditId": decision.audit_id,
            "decision": decision.decision,
            "notes": decision.notes,
            "reviewerName": decision.reviewer_name,
            "createdAt": decision.created_at,
        }
