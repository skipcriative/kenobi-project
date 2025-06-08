#kenobi/persistence/entities/email_log_entity.py

from sqlalchemy import Column, String, Text, DateTime, Integer
from kenobi.persistence.base import Base
import uuid
from datetime import datetime, timedelta, timezone

UTC_menos_3 = timezone(timedelta(hours=3))

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(String(20), primary_key=True, default=lambda: str(uuid.uuid4()))
    sent_at = Column(DateTime, default=lambda: datetime.now(UTC_menos_3))
    subject = Column(String(255))
    recipients = Column(Text)
    raw_payload = Column(Text)
    opportunities = Column(Text)
    html_content = Column(Text)
    status = Column(String(20))
    error_message = Column(Text, nullable=True)
    api_response_code = Column(Integer, nullable=True)
