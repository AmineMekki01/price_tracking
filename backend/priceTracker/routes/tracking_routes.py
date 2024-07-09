from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from priceTracker.components.database import get_db
from priceTracker.components.models import ProductResult, PriceHistory
from datetime import datetime
import redis
import json

router = APIRouter()
redis_client = redis.Redis(host='127.0.0.1', port=6380, db=0)


@router.post("/track")
async def track_product(data: dict = Body(...), db: Session = Depends(get_db)):
    product_id = data.get("product_id")
    search_text = data.get("search_text")
    if not product_id:
        raise HTTPException(status_code=422, detail="Product ID is required")

    cached_data = redis_client.get(search_text)
    if not cached_data:
        raise HTTPException(status_code=404, detail="Product data not found in cache. Search for the product first.")

    product_list = json.loads(cached_data)
    product_data = next((item for item in product_list if item['id'] == product_id), None)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product ID not found in cached data")

    product = db.query(ProductResult).filter(ProductResult.id == product_id).first()
    print(f"""Product: {product}""")
    if not product:
        product = ProductResult(
            id=product_id,
            name=product_data['product_name'],
            img=product_data['img'],
            url=product_data['url'],
            price=product_data['price'],
            currency=product_data['currency'],
            search_text=search_text,
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
            
    return {"status": "tracking started"}

@router.get("/tracked-products")
async def get_tracked_products(db: Session = Depends(get_db)):
    products = db.query(ProductResult).all()
    return products

@router.get("/price-history/{product_id}")
async def get_price_history(product_id: str, db: Session = Depends(get_db)):
    product = db.query(ProductResult).filter(ProductResult.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    price_history = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()
    return {"product": product, "price_history": price_history}


