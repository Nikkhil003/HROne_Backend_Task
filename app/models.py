from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Product Models ---

class SizeQuantity(BaseModel):
    """Model for product size and quantity information."""
    size: str = Field(..., description="Size of the product (e.g., 'small', 'medium', 'large')")
    quantity: int = Field(..., ge=0, description="Available quantity for this size")

class ProductCreate(BaseModel):
    """Request model for creating a new product."""
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    sizes: List[SizeQuantity] = Field(..., min_items=1)

class ProductResponse(BaseModel):
    """Response model for product creation."""
    id: str = Field(..., description="Unique identifier of the created product")

class ProductListDetails(BaseModel):
    """Model for product details in list responses."""
    id: str = Field(..., description="Unique identifier of the product")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")

class Pagination(BaseModel):
    """Model for pagination information."""
    next: Optional[str] = Field(None, description="Next page offset (as string)")
    limit: int = Field(..., description="Number of items requested")
    offset: int = Field(..., description="Number of items skipped")
    previous: Optional[str] = Field(None, description="Previous page offset (as string)")

class ProductListResponse(BaseModel):
    """Response model for product listing with pagination."""
    data: List[ProductListDetails] = Field(..., description="List of products")
    page: Pagination = Field(..., description="Pagination information")

# --- Order Models ---

class OrderItemCreate(BaseModel):
    """Model for order items in order creation requests."""
    productId: str = Field(..., description="Product ID")
    qty: int = Field(..., gt=0, description="Quantity to order")

class OrderCreate(BaseModel):
    """Request model for creating a new order."""
    userId: str = Field(..., description="User ID placing the order")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="List of items to order")

class OrderResponse(BaseModel):
    """Response model for order creation."""
    id: str = Field(..., description="Unique identifier of the created order")

class ProductDetails(BaseModel):
    """Model for basic product information in order responses."""
    id: str = Field(..., description="Product unique identifier")
    name: str = Field(..., description="Product name")

class OrderItemDetails(BaseModel):
    """Model for order item details in order list responses."""
    productDetails: ProductDetails = Field(..., description="Product information")
    qty: int = Field(..., description="Quantity ordered")

class OrderListDetails(BaseModel):
    """Model for order details in list responses."""
    id: str = Field(..., description="Order unique identifier")
    items: List[OrderItemDetails] = Field(..., description="List of items in the order")
    total: float = Field(..., description="Total order amount")

class OrderListResponse(BaseModel):
    """Response model for order listing with pagination."""
    data: List[OrderListDetails] = Field(..., description="List of orders")
    page: Pagination = Field(..., description="Pagination information")

# --- Query Parameter Models ---

class ProductQueryParams(BaseModel):
    """Model for product listing query parameters."""
    name: Optional[str] = Field(None, description="Product name filter (supports partial search)", max_length=100)
    size: Optional[str] = Field(None, description="Filter by size (e.g., 'large')", max_length=20)
    limit: int = Field(10, ge=1, le=100, description="Number of products to return")
    offset: int = Field(0, ge=0, description="Number of products to skip")

class OrderQueryParams(BaseModel):
    """Model for order listing query parameters."""
    limit: int = Field(10, ge=1, le=100, description="Number of orders to return") 
    offset: int = Field(0, ge=0, description="Number of orders to skip")