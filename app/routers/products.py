from fastapi import APIRouter, status, Query, HTTPException
from typing import Optional
from bson import ObjectId
import re
from .. import models, database

router = APIRouter()
products_collection = database.db["products"]

@router.post("/products", response_model=models.ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: models.ProductCreate):
    """
    Create a new product with a name, price, and available sizes/quantities.
    
    Args:
        product: Product data including name, price, and size/quantity combinations
        
    Returns:
        ProductResponse: Contains the ID of the newly created product
        
    Raises:
        HTTPException: If validation fails or database operation fails
    """
    try:
        # Validate business rules
        if product.price <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than 0")
        
        if not product.sizes:
            raise HTTPException(status_code=400, detail="At least one size must be provided")
        
        for size_item in product.sizes:
            if size_item.quantity < 0:
                raise HTTPException(status_code=400, detail="Quantity cannot be negative")
        
        # Use model_dump() instead of dict() for newer Pydantic versions
        result = await products_collection.insert_one(product.model_dump())
        return {"id": str(result.inserted_id)}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create product")

@router.get("/products", response_model=models.ProductListResponse)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    """
    List products with optional filters and pagination.
    
    Args:
        name: Optional filter by product name (supports partial, case-insensitive search)
        size: Optional filter by available product size
        limit: Number of documents to return (max 100)
        offset: Number of documents to skip for pagination
        
    Returns:
        ProductListResponse: Paginated list of products with basic details
        
    Raises:
        HTTPException: If validation fails or database operation fails
    """
    try:
        query = {}
        if name:
            # Trim whitespace and validate
            name = name.strip()
            if len(name) > 100:  # Prevent overly long search terms
                raise HTTPException(status_code=400, detail="Search term too long")
            query["name"] = {"$regex": re.escape(name), "$options": "i"}
        
        if size:
            size = size.strip()
            if len(size) > 20:  # Reasonable size limit
                raise HTTPException(status_code=400, detail="Size parameter too long")
            query["sizes.size"] = size

        # Fetch only the required fields for the list view
        cursor = products_collection.find(query, {"_id": 1, "name": 1, "price": 1}).skip(offset).limit(limit)
        
        product_list = [
            models.ProductListDetails(id=str(doc["_id"]), name=doc["name"], price=doc["price"])
            async for doc in cursor
        ]

        # Pagination logic
        next_offset_str = str(offset + limit) if len(product_list) == limit else None
        prev_offset_str = str(offset - limit) if offset > 0 else None

        return {
            "data": product_list,
            "page": {
                "next": next_offset_str,
                "limit": limit,
                "offset": offset,
                "previous": prev_offset_str,
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve products")