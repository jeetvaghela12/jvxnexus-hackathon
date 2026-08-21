from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.database import get_db
from api.auth_routes import get_current_user
from models.user_model import User
from models.clientshield_model import ClientShieldReport
from services.client_risk_providers import check_domain_age, check_mx_record, check_disposable_email
from services.clientshield_engine import calculate_risk
from services.audit_storage import store_report_to_s3
from pydantic import BaseModel

router = APIRouter(prefix="/clientshield", tags=["clientshield"])

class CheckRequest(BaseModel):
    client_name: str
    client_domain: str
    client_email_domain: str

@router.post("/check")
def check_client(payload: CheckRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    domain_age = check_domain_age(payload.client_domain)
    mx_valid = check_mx_record(payload.client_domain)
    disposable = check_disposable_email(payload.client_email_domain)
    result = calculate_risk(payload.client_name, domain_age, None, mx_valid, disposable)
    report = ClientShieldReport(
        user_id=current_user.id, client_name=payload.client_name, client_domain=payload.client_domain,
        domain_age_days=domain_age, registry_match_found=None, sanctions_hit=result["sanctions_hit"],
        mx_valid=mx_valid, disposable_email=disposable, risk_score=result["risk_score"], risk_points=result["risk_points"],
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    s3_result = store_report_to_s3({"id": report.id, "client_name": report.client_name, "risk_score": report.risk_score, "created_at": report.created_at})
    return {
        "id": report.id, "client_name": report.client_name, "client_domain": report.client_domain,
        "domain_age_days": report.domain_age_days, "sanctions_hit": report.sanctions_hit,
        "mx_valid": report.mx_valid, "disposable_email": report.disposable_email,
        "risk_score": report.risk_score, "risk_points": report.risk_points,
        "created_at": report.created_at, "s3_stored": s3_result.get("stored", False),
        "reasoning": result["reasoning"],
    }