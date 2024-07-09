"""
File : backend/priceTracker/routes/product_routes.py
Description : This file contains the routes for the product endpoints. The search_product function is used to search for a product on the specified platforms. The platforms parameter is a list of strings that specifies the platforms to search on. The function returns a list of dictionaries containing the product information for each platform.
"""
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from priceTracker.components.scraper.amazon import scrape_amazon, scrape_amazon_product_page
from priceTracker.components.database import get_db
from priceTracker.components.models import ProductResult, PriceHistory

router = APIRouter()

@router.get("/search")
async def search_product(product_name: str, platforms: list[str] = ["amazon"], db: Session = Depends(get_db)):
    results = []
    if 'amazon' in platforms:
        results.extend(scrape_amazon(db, product_name))
    return results

@router.post("/search-product-url")
async def search_product_url_price(data: dict = Body(...), db: Session = Depends(get_db)):
    url = data.get("url")
    if not url:
        raise HTTPException(status_code=422, detail="URL is required")
    
    product_data = scrape_amazon_product_page(db, url=url)
    if product_data:
        product_id = product_data["id"]
        product = db.query(ProductResult).filter(ProductResult.url == url).first()
        if not product:
            product = ProductResult(
                id=product_id,
                name=product_data['product_name'],
                img=product_data['img'],
                url=product_data['url'],
                price=product_data['price'],
                currency=product_data['currency'],
                search_text="",
                source='Amazon'
            )
            db.add(product)
            db.commit()
            db.refresh(product)
            
            price_history = PriceHistory(
                product_id=product.id,
                price=product.price,
                currency=product.currency
            )
            db.add(price_history)
            db.commit()
            db.refresh(price_history)
    return product_data