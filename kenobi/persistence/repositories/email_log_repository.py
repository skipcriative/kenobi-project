#kenobi/db/repositories/email_log_repository.py
from kenobi.persistence import SessionLocal
from kenobi.persistence.entities.email_log_entity import EmailLog
from kenobi.dtos.email_log_dto import EmailLogDTO

def save_email_log(data: dict) -> EmailLogDTO:
    session = SessionLocal()
    try:
        log = EmailLog(**data)
        session.add(log)
        session.flush()  # Garante que o ID é atribuído

        dto = EmailLog(log)  # Ainda está vinculado à sessão
        session.commit()
        return dto
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_email_log_by_id(log_id: str):
    session = SessionLocal()
    try:
        return session.query(EmailLog).filter(EmailLog.id == log_id).first()
    finally:
        session.close()

def get_all_email_logs_paginated(skip: int = 0, limit: int = 10):
    session = SessionLocal()
    try:
        return session.query(EmailLog).offset(skip).limit(limit).all()
    finally:
        session.close()