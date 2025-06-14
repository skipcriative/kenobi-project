#kenobi/db/repositories/audit_event_repository.py

import logging
from kenobi.persistence import SessionLocal
from kenobi.persistence.entities.audit_event_entity import AuditEvent
from kenobi.dtos.audit_event_dto import AuditEventDTO

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def save_audit_event(data: dict) -> AuditEvent:
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        event = AuditEvent(**data)
        session.add(event)
        session.flush()

        entity = AuditEvent.copy(event)
        session.commit()
        logger.info("Data commited to DB.")
        return entity
    except Exception as e:
        logger.exception(f"Data cloud not be saved. Raised exception: {e}")
        session.rollback()
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")


def get_audit_event_by_id(audit_id: str):
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        entity = session.query(AuditEvent).filter(AuditEvent.id == audit_id).first()
        logger.info(f"Entity recovered from DB.")
        return entity
    except Exception as e:
        logger.exception(f"Data cloud not be recovered. Raised exception: {e}")
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")


def get_all_audit_events_paginated(skip: int = 0, limit: int = 10):
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        entities = session.query(AuditEvent).offset(skip).limit(limit).all()
        logger.info(f"Number of entities recovered: {len(entities)}")
        return entities
    except Exception as e:
        logger.exception(f"Data cloud not be recovered. Raised exception: {e}")
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")