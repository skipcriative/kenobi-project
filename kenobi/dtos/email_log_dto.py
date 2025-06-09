#kenobi/dtos/email_log_dto.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EmailLogDTO:
    id: Optional[int] = None
    subject: str = ""
    recipients: str = ""
    raw_payload: str = ""
    opportunities: str = ""
    html_content: str = ""
    status: str = ""
    error_message: Optional[str] = None
    api_response_code: int = ""
    sent_at: datetime = None

    @staticmethod
    def from_entity(entity) -> "EmailLogDTO":
        return EmailLogDTO(
            id=entity.id,
            subject=entity.subject,
            recipients=entity.recipients,
            raw_payload=entity.raw_payload,
            opportunities=entity.opportunities,
            html_content=entity.html_content,
            status=entity.status,
            sent_at=entity.sent_at,
            error_message=entity.error_message,
            api_response_code=entity.api_response_code,
        )