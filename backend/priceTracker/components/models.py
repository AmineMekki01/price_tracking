"""
File: backend/priceTracker/components/models.py
Description : This file contains the model for the product results table.
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from priceTracker.components.database import Base
import uuid

class ProductResult(Base):
    __tablename__ = 'product_results'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(1000))
    img = Column(String(1000))
    url = Column(String(1000))
    price = Column(String(255))
    currency = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    search_text = Column(String(255))
    source = Column(String(255))
    last_checked = Column(DateTime, nullable=True)

    def __init__(self, id, name, img, url, price, currency, search_text, source):
        self.id = id
        self.name = name
        self.url = url
        self.img = img
        self.price = price
        self.currency = currency
        self.search_text = search_text
        self.source = source
        
class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('product_results.id'))
    price = Column(String(255))
    currency = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, product_id, price, currency, created_at=datetime.utcnow()):
        self.product_id = product_id
        self.price = price
        self.currency = currency
        self.created_at = created_at