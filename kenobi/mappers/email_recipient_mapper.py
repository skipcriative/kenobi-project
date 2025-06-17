#kenobi/mappers/email_recipient_mapper.py
import logging
from kenobi.persistence.entities import EmailRecipient
from kenobi.dtos import EmailRecipientDTO

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def dto_to_entity(dto: EmailRecipientDTO) -> EmailRecipient:
    return EmailRecipient(
        id = dto.id,
        email_group = dto.email_group,
        email = dto.email
    )