#kenobi/dtos/email_log_dto.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EmailRecipientDTO:
    id: Optional[int] = None
    email_group: str = ""
    email: str = ""
    active: bool = None

    @staticmethod
    def from_entity(entity) -> "EmailRecipientDTO":
        return EmailRecipientDTO(
            id=entity.id,
            email_group=entity.email_group,
            email=entity.email,
            active= entity.active
        )