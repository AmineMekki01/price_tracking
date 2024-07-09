from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from priceTracker.components.database import SessionLocal
from priceTracker.components.scraper.amazon import scrape_amazon_price
from priceTracker.components.models import ProductResult, PriceHistory
from priceTracker import logger

def update_tracked_products():
    db: Session = SessionLocal()
    try:
        products = db.query(ProductResult).all()
        for product in products:
            product_price = scrape_amazon_price(db, product.url)
            if product_price:
                price_history = PriceHistory(
                    product_id=product.id,
                    price=product_price,
                    currency=product.currency
                )
                db.add(price_history)
                db.commit()
                db.refresh(price_history)
                logger.info(f"Added price history for product {product.id}")
    except Exception as e:
        logger.error(f"Error updating tracked products: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_tracked_products, 'interval', minutes=1)
    scheduler.start()
    logger.info("Scheduler started")

