#kenobi/services/email_logs_service.py

from datetime import datetime, timedelta, timezone
from kenobi.dtos.email_log_dto import EmailLogDTO
from kenobi.persistence.repositories import email_log_repository

def create_email_log(dto: EmailLogDTO):
    data = {
        "subject": dto.subject,
        "recipients": dto.recipients,
        "raw_payload": dto.raw_payload,
        "opportunities": dto.opportunities,
        "html_content": dto.html_content,
        "status": dto.status,
        "error_message": dto.error_message,
        "sent_at": dto.sent_at,
        "api_response_code" : dto.api_response_code
    }
    saved = email_log_repository.save_email_log(data)
    return EmailLogDTO.from_entity(saved)

#untested
def get_email_log_by_id(log_id: int) -> EmailLogDTO:
    log = email_log_repository.get_email_log_by_id(log_id)
    return EmailLogDTO.from_entity(log) if log else None

def get_all_email_logs_paginated(skip: int = 0, limit: int = 10):
    logs = email_log_repository.get_all_email_logs_paginated(skip, limit)
    return [EmailLogDTO(**log.__dict__) for log in logs]
