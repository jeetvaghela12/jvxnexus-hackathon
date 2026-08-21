from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.database import get_db
from api.auth_routes import get_current_user
from models.user_model import User
from models.clientshield_model import ClientShieldReport
from services.client_risk_providers import check_domain_age, check_mx_record, check_disposable_email
from services.clientshield_engine import calculate_risk
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
    return report

@router.get("/reports")
def list_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.execute(select(ClientShieldReport).where(ClientShieldReport.user_id == current_user.id)).scalars().all()