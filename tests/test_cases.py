import os
os.environ["DATABASE_URL"] = "sqlite:///./test_wmo.db"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

BASE = {
    "citizenId": "SYNTH-001",
    "name": "Test Persoon",
    "address": "Teststraat 1",
    "birthDate": "1955-01-01",
    "ageGroup": "65-74",
    "requestedProvision": "huishoudelijke_hulp",
    "problemDescription": "Beperkte mobiliteit en hulp nodig bij zwaar huishoudelijk werk.",
    "severity": "laag",
    "multipleProblems": False,
    "aiConsent": True
}


def test_dashboard_is_available():
    r = client.get("/")
    assert r.status_code == 200
    assert "WMO Kompas" in r.text


def test_1_low_risk_auto_message():
    r = client.post("/process", json=BASE)
    assert r.status_code == 200
    data = r.json()
    assert data["route"] == "automatic_message"
    assert data["fairness"]["passed"] is True


def test_2_high_risk_human_review():
    p = BASE | {"severity": "hoog", "multipleProblems": True}
    r = client.post("/process", json=p)
    assert r.status_code == 200
    assert r.json()["route"] == "human_review"


def test_3_fairness_flag_human_review():
    p = BASE | {"injectForbiddenTermForTest": "religie"}
    r = client.post("/process", json=p)
    assert r.status_code == 200
    data = r.json()
    assert data["fairness"]["passed"] is False
    assert "religie" in data["fairness"]["forbiddenTerms"]
    assert data["route"] == "human_review"


def test_4_no_ai_consent_validation_error():
    p = BASE | {"aiConsent": False}
    r = client.post("/process", json=p)
    assert r.status_code == 422
    assert "AI-toestemming ontbreekt" in str(r.json())


def test_structured_pii_never_crosses_ai_boundary():
    p = BASE | {
        "problemDescription": (
            "Test Persoon van Teststraat 1, 1955-01-01, test@example.nl en "
            "06-12345678 heeft ondersteuning nodig."
        )
    }
    r = client.post("/process", json=p)
    assert r.status_code == 200
    minimized = r.json()["minimizedApplication"]
    serialized = str(minimized).lower()
    for forbidden in ["test persoon", "teststraat 1", "1955-01-01", "test@example.nl", "06-12345678"]:
        assert forbidden not in serialized
    assert "persoonsgegeven verwijderd" in serialized


def test_audit_contains_required_decision_fields():
    process_response = client.post("/process", json=BASE)
    assert process_response.status_code == 200
    audit_id = process_response.json()["audit"]["auditId"]

    records = client.get("/audit")
    assert records.status_code == 200
    record = next(row for row in records.json() if row["id"] == audit_id)
    assert record["citizenToken"].startswith("CIT-")
    assert record["risk"] == "laag"
    assert record["riskScore"] == 0.15
    assert record["flags"]["fairness"]["passed"] is True
    assert record["proposal"]
    assert record["rationale"]
    assert record["route"] == "automatic_message"
