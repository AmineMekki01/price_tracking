"""
This file contains the routes for the product endpoints. The search_product function is used to search for a product on the specified platforms. The platforms parameter is a list of strings that specifies the platforms to search on. The function returns a list of dictionaries containing the product information for each platform.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from priceTracker.components.scraper.amazon import scrape_amazon
from priceTracker.components.database import get_db

router = APIRouter()

@router.get("/search")
async def search_product(product_name: str, platforms: list[str] = ["amazon"], db: Session = Depends(get_db)):
    results = []
    if 'amazon' in platforms:
        results.extend(scrape_amazon(db, product_name))
    return results