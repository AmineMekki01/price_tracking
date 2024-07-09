"""
File : backend/priceTracker/entity/config_entity.py
Description : This file contains the dataclasses for the configuration entities.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class DatabaseConfig:
    DATABASE_NAME : str
    DATABASE_USER : str
    DATABASE_PASSWORD : str
    DATABASE_HOST : str
    DATABASE_PORT : str
    DATABASE_URL : str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool 
