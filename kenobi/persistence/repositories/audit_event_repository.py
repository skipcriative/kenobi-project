#kenobi/db/repositories/audit_event_repository.py
from kenobi.persistence import SessionLocal
from kenobi.persistence.entities.audit_event_entity import AuditEvent
from kenobi.dtos.audit_event_dto import AuditEventDTO

def save_audit_event(data: dict) -> AuditEvent:
    session = SessionLocal()
    try:
        event = AuditEvent(**data)
        session.add(event)
        session.flush()

        entity = AuditEvent.copy(event)
        session.commit()
        return entity
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_audit_events_by_type(event_type: str):
    session = SessionLocal()
    try:
        return session.query(AuditEvent).filter(AuditEvent.event_type == event_type).all()
    finally:
        session.close()


def get_all_audit_events_paginated(skip: int = 0, limit: int = 10):
    session = SessionLocal()
    try:
        return session.query(AuditEvent).offset(skip).limit(limit).all()
    finally:
        session.close()
