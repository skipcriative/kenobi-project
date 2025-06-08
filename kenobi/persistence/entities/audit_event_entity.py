#kenobi/db/entities/audit_event_entity.py
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from kenobi.persistence.base import Base
import uuid
from datetime import datetime, timezone, timedelta

UTC_menos_3 = timezone(timedelta(hours=3))

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(String(20), primary_key=True, default=lambda: str(uuid.uuid4()))

    timestamp = Column(DateTime, default=lambda: datetime.now(UTC_menos_3))
    event_type = Column(String(100))
    status_code = Column(String(20))
    resume = Column(Text)
    message = Column(Text)
    data = Column(Text)

    #optional relation to EmailLog
    email_log_id = Column(String(20), ForeignKey("email_logs.id"), nullable = True)
