#kenobi/db/entities/audit_event_entity.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from kenobi.persistence.base import Base
import uuid
from zoneinfo import ZoneInfo
from datetime import datetime, timezone, timedelta

BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(20), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(BRAZIL_TZ))
    event_type = Column(String(100))
    status_code = Column(String(20))
    resume = Column(Text)
    message = Column(Text)
    data = Column(Text)

    #optional relation to EmailLog
    email_log_id = Column(String(20), ForeignKey("email_logs.id"), nullable = True)

    @classmethod
    def copy(cls, other: "AuditEvent") -> "AuditEvent":
        return cls(
            id=other.id,
            timestamp=other.timestamp,
            event_type=other.event_type,
            status_code=other.status_code,
            resume=other.resume,
            message=other.message,
            data=other.data,
            email_log_id=other.email_log_id
        )