#kenobi/config/db_config.py

import os
from sqlalchemy import create_engine
from kenobi.persistence.base import Base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


#load enviroment variables
load_dotenv()

#use the enviroment variable for database_url
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kenobi.db")

#create engine sqlalchemy
engine = create_engine(DATABASE_URL)

#create local session
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

#Automatically creates tables if they don't exist
def init_db():
    from kenobi.persistence.entities import AuditEvent, EmailLog

    print("🧪 Tabelas encontradas no metadata:")
    print(Base.metadata.tables.keys())

    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()
