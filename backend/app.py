# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from priceTracker.components.database import Base, engine
from priceTracker.routes.product_routes import router as product_router
from priceTracker.routes.tracking_routes import router as tracking_routes

from priceTracker.scheduler.product_price_update import start_scheduler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(product_router, prefix="/api")
app.include_router(tracking_routes, prefix="/api")

# @app.on_event("startup")
# async def startup_event():
#     start_scheduler()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
