"""
This file contains the model for the product results table.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from priceTracker.components.database import Base

class ProductResult(Base):
    __tablename__ = 'product_results'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(1000))
    img = Column(String(1000))
    url = Column(String(1000))
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    search_text = Column(String(255))
    source = Column(String(255))

    def __init__(self, name, img, url, price, search_text, source):
        self.name = name
        self.url = url
        self.img = img
        self.price = price
        self.search_text = search_text
        self.source = source
