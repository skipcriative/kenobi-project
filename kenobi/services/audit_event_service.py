#kenobi/services/audit_event_service.py

from datetime import datetime, timedelta, timezone
from kenobi.dtos.audit_event_dto import AuditEventDTO
from kenobi.persistence.repositories import audit_event_repository

UTC_menos_3 = timezone(timedelta(hours=3))

def create_audit_event(dto: AuditEventDTO):
    data = {
        "event_type": dto.event_type,
        "resume": dto.resume,
        "message": dto.message,
        "status_code": dto.status_code,
        "timestamp": dto.timestamp or datetime.now(UTC_menos_3),
        "data": dto.data,
        "email_log_id": dto.email_log_id
    }
    saved = audit_event_repository.save_audit_event(data)
    return saved #AuditEventDTO(**saved.__dict__)

def get_audit_events_by_type(event_type: str):
    events = audit_event_repository.get_audit_events_by_type(event_type)
    return [AuditEventDTO(**e.__dict__) for e in events]

def get_all_audit_events_paginated(skip: int = 0, limit: int = 10):
    events = audit_event_repository.get_all_audit_events_paginated(skip, limit)
    return [AuditEventDTO(**e.__dict__) for e in events]
