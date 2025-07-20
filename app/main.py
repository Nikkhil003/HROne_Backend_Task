from fastapi import FastAPI
from .routers import products, orders

app = FastAPI(
    title="HROne E-commerce Backend Task",
    description="This API provides endpoints to manage products and orders for an e-commerce application.",
    version="1.0.0"
)

# Include routers for different parts of the API
app.include_router(products.router, tags=["Products"])
app.include_router(orders.router, tags=["Orders"])

@app.get("/", tags=["Root"])
async def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the E-commerce Application!"}