#kenobi/services/audit_event_service.py

import logging
from datetime import datetime, timedelta, timezone
from kenobi.dtos.audit_event_dto import AuditEventDTO
from kenobi.persistence.repositories import audit_event_repository

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_audit_event(dto: AuditEventDTO):

    logger.info("Started create audit log on DB.")

    data = {
        "event_type": dto.event_type,
        "resume": dto.resume,
        "message": dto.message,
        "status_code": dto.status_code,
        "timestamp": dto.timestamp,
        "data": dto.data,
        "email_log_id": dto.email_log_id
    }
    saved = audit_event_repository.save_audit_event(data)

    logger.info(f"Audit log created with ID: {saved.id}")

    return AuditEventDTO.from_entity(saved)

#untested
def get_audit_event_by_id(audit_id: str):
    logger.info("Started GET Audit log on DB.")
    audit = audit_event_repository.get_audit_event_by_id(audit_id)
    return AuditEventDTO.from_entity(audit) if audit else None

def get_all_audit_events_paginated(skip: int = 0, limit: int = 10):
    logger.info("Started GET ALL Audit log on DB.")
    audits = audit_event_repository.get_all_audit_events_paginated(skip, limit)
    return [AuditEventDTO.from_entity(audit) for audit in audits]
