#kenobi/persistence/entities/email_recipient_entity
from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean
from zoneinfo import ZoneInfo
from datetime import datetime
import uuid
from kenobi.persistence.base import Base

Brazil_TZ = ZoneInfo("America/Sao_Paulo")

class EmailRecipient(Base):
    __tablename__ = "email_recipients"

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    email_group = Column(String(255), nullable=True)
    email = Column(String(255))
    active = Column(Boolean, nullable=False, default=True)

    #optional relation to user
    #user_id = Column(String(50), ForeignKey("user.id"), nullable = True)

    @classmethod
    def copy(cls, other: "EmailRecipient") -> "EmailRecipient":
        return cls(
            id = other.id,
            email_group = other.email_group,
            email = other.email,
            active = other.active
        )
    

