#kenobi/db/repositories/email_log_repository.py

import logging
from kenobi.persistence import SessionLocal
from kenobi.persistence.entities.email_log_entity import EmailLog
from kenobi.dtos.email_log_dto import EmailLogDTO

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def save_email_log(data: dict) -> EmailLog:
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        log = EmailLog(**data)
        session.add(log)
        session.flush()  # Garante que o ID é atribuído

        entity = EmailLog.copy(log)  # Ainda está vinculado à sessão
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


def get_email_log_by_id(log_id: str):
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        entity = session.query(EmailLog).filter(EmailLog.id == log_id).first()
        logger.info(f"Entity recovered from DB.")
        return entity
    except Exception as e:
        logger.exception(f"Data cloud not be recovered. Raised exception: {e}")
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")

def get_all_email_logs_paginated(skip: int = 0, limit: int = 10):
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        entities = session.query(EmailLog).offset(skip).limit(limit).all()
        logger.info(f"Number of entities recovered: {len(entities)}")
        return entities
    except Exception as e:
        logger.exception(f"Data cloud not be recovered. Raised exception: {e}")
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")