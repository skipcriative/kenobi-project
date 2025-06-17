#kenobi/services/email_logs_service.py

import logging
from kenobi.dtos import EmailRecipientDTO
from kenobi.persistence.repositories import email_recipient_repository
from kenobi.mappers import dto_to_entity as emailRecipientDTO_To_Entity

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_email_recipient(dto: EmailRecipientDTO):

    logger.info("Started create email recipient on DB.")

    data = emailRecipientDTO_To_Entity(dto)

    saved = email_recipient_repository.save_email_recipient(data)

    logger.info(f"Email Recipient created with ID: {saved.id}")

    return EmailRecipientDTO.from_entity(saved)

#untested
def get_all_email_recipient_paginated(skip: int = 0, limit: int = 10):

    logger.info("Started GET ALL email log on DB.")

    emails = email_recipient_repository.get_all_email_recipients_paginated(skip, limit)

    return [EmailRecipientDTO.from_entity(email) for email in emails]


