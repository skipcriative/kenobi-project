#kenobi/persistence/entities/email_log_entity.py

from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.types import TIMESTAMP
from zoneinfo import ZoneInfo
from kenobi.persistence.base import Base
import uuid
from datetime import datetime, timedelta, timezone

BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(String(20), primary_key=True, default=lambda: str(uuid.uuid4()))
    sent_at = Column(DateTime(timezone=True), default=lambda: datetime.now(BRAZIL_TZ))
    subject = Column(String(255))
    recipients = Column(Text)
    raw_payload = Column(Text)
    opportunities = Column(Text)
    html_content = Column(Text)
    status = Column(String(20))
    error_message = Column(Text, nullable=True)
    api_response_code = Column(Integer, nullable=True)

    @classmethod
    def copy(cls, other: "EmailLog") -> "EmailLog":
        return cls(
            id=other.id,
            sent_at=other.sent_at,
            subject=other.subject,
            recipients=other.recipients,
            raw_payload=other.raw_payload,
            opportunities=other.opportunities,
            html_content=other.html_content,
            status=other.status,
            error_message=other.error_message,
            api_response_code=other.api_response_code,
        )