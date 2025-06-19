#kenobi/config/db_config.py

import os
from sqlalchemy import create_engine
from kenobi.persistence.base import Base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging


#load enviroment variables
load_dotenv(override=True)

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

#use the enviroment variable for database_url
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kenobi.db")

#create engine sqlalchemy
logger.info("Creating DB engine.")
engine = create_engine(DATABASE_URL)

#create local session
logger.info("Creating Local Session.")
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#Automatically creates tables if they don't exist
def init_db():
    from kenobi.persistence.entities import AuditEvent, EmailLog, EmailRecipient

    logger.info("Importing tables.")
    logger.info(f"Tables found on metadata:{Base.metadata.tables.keys()}")

    Base.metadata.create_all(bind=engine)
    logger.info("Tables created with success")

if __name__ == "__main__":
    init_db()
