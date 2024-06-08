from fastapi import FastAPI
from priceTracker.components.database import Base, engine
from priceTracker.routes.product_routes import router as product_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(product_router, prefix="/api")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
