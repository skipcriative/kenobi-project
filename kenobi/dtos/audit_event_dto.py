#kenobi/dtos/audit_event_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class AuditEventDTO:
    id: Optional[int] = None
    event_type: str = ""
    resume: str = ""
    message: str = ""
    status_code: str = ""
    timestamp: datetime = None
    data: str = ""
    email_log_id: Optional[int] = None  # pode ser nulo

    @staticmethod
    def from_entity(entity) -> "AuditEventDTO":
        return AuditEventDTO(
            id=entity.id,
            event_type=entity.event_type,
            resume=entity.resume,
            message=entity.message,
            status_code=entity.status_code,
            timestamp=entity.timestamp,
            data=entity.data,
            email_log_id=entity.email_log_id,
        )