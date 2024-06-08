""" 
This module is responsible for creating the database connection and session.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from priceTracker.config.configuration import ConfigurationManager

config_manager = ConfigurationManager()
database_config = config_manager.get_database_config()

engine = create_engine(database_config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()