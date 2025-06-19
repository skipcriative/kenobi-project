#kenobi/scripts/seed_email_recipients_db.py

import logging
from kenobi.dtos import EmailRecipientDTO
from kenobi.services import email_recipient_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Email Recipients database seed.")

    #creating beta users
    beta_users_data = [
        EmailRecipientDTO(
            email_group="beta",
            email="eduardo.lemos16@gmail.com", 
            active=True
        ),

        EmailRecipientDTO(
            email_group="beta",
            email="eduardo.lemos@gruposkip.com", 
            active=True
        ),

        EmailRecipientDTO(
            email_group="beta",
            email="thalles.carvalho@gruposkip.com", 
            active=True
        ),

        EmailRecipientDTO(
            email_group="beta",
            email="lizmatiaslisboa@gmail.com ", 
            active=True
        ),

        EmailRecipientDTO(
            email_group="beta",
            email="projetos.vas@gmail.com", 
            active=True
        )
    ]

    #persiste data
    for dto in beta_users_data:
        response = email_recipient_service.create_email_recipient(dto)
    
    logger.info("Email Recipient Database seed completed Successfully")

if __name__ =="__main__":
    main()