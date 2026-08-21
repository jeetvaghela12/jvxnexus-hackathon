from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from core.database import Base

class ClientShieldReport(Base):
    __tablename__ = "clientshield_reports"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    client_name: Mapped[str] = mapped_column(String)
    client_domain: Mapped[str] = mapped_column(String)
    domain_age_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    registry_match_found: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    sanctions_hit: Mapped[bool] = mapped_column(Boolean, default=False)
    mx_valid: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    disposable_email: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    risk_score: Mapped[str] = mapped_column(String)
    risk_points: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))