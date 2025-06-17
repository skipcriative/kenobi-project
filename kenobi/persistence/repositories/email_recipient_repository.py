#kenobi/persistence/repositories/email_recipient_repository

import logging
from kenobi.persistence import SessionLocal
from kenobi.persistence.entities.email_recipient_entity import EmailRecipient

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def save_email_recipient(data: EmailRecipient) -> EmailRecipient:
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        entity = data
        session.add(entity)
        session.flush()  # Garante que o ID é atribuído

        response = EmailRecipient.copy(entity)  # Ainda está vinculado à sessão
        session.commit()
        logger.info("Data commited to DB.")
        return response
    except Exception as e:
        logger.exception(f"Data cloud not be saved. Raised exception: {e}")
        session.rollback()
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")

def get_all_email_recipients_paginated(skip: int = 0, limit: int = 10):
    session = SessionLocal()
    logger.info("DB Session Open.")
    try:
        entities = session.query(EmailRecipient).offset(skip).limit(limit).all()
        logger.info(f"Number of entities recovered: {len(entities)}")
        return entities
    except Exception as e:
        logger.exception(f"Data cloud not be recovered. Raised exception: {e}")
        raise e
    finally:
        session.close()
        logger.info("DB Session Closed.")