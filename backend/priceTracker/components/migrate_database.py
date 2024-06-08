""" 
This script is used to create the database schema.
"""
from priceTracker.components.database import Base, engine

Base.metadata.create_all(bind=engine)
