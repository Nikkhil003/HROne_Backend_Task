from fastapi import APIRouter, status, Path, Query, HTTPException
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
from .. import models, database

router = APIRouter()
orders_collection = database.db["orders"]
products_collection = database.db["products"]

@router.post("/orders", response_model=models.OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: models.OrderCreate):
    """
    Create a new order for a specific user with a list of items.
    
    Args:
        order: Order data including user ID and list of items with product IDs and quantities
        
    Returns:
        OrderResponse: Contains the ID of the newly created order
        
    Raises:
        HTTPException: If validation fails or database operation fails
    """
    try:
        # Validate business rules
        if not order.items:
            raise HTTPException(status_code=400, detail="Order must contain at least one item")
        
        if not order.userId.strip():
            raise HTTPException(status_code=400, detail="User ID cannot be empty")
        
        # Convert product IDs from string to ObjectId and validate them
        order_dict = order.model_dump()
        product_ids = []
        
        for item in order_dict["items"]:
            if item["qty"] <= 0:
                raise HTTPException(status_code=400, detail="Item quantity must be greater than 0")
            
            try:
                product_id = ObjectId(item["productId"])
                item["productId"] = product_id
                product_ids.append(product_id)
            except InvalidId:
                raise HTTPException(status_code=400, detail=f"Invalid product ID: {item['productId']}")
        
        # Verify that all products exist
        existing_products = await products_collection.count_documents({"_id": {"$in": product_ids}})
        if existing_products != len(product_ids):
            raise HTTPException(status_code=400, detail="One or more products do not exist")
        
        result = await orders_collection.insert_one(order_dict)
        return {"id": str(result.inserted_id)}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create order")

@router.get("/orders/{user_id}", response_model=models.OrderListResponse)
async def get_user_orders(
    user_id: str = Path(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=100),  # Add upper limit
    offset: int = Query(0, ge=0)
):
    """
    Get a list of orders for a specific user with pagination.
    
    Args:
        user_id: The ID of the user whose orders to retrieve
        limit: Number of orders to return (max 100)
        offset: Number of orders to skip for pagination
        
    Returns:
        OrderListResponse: Paginated list of orders with product details and totals
        
    Raises:
        HTTPException: If validation fails or database operation fails
    """
    try:
        # Validate user_id
        user_id = user_id.strip()
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID cannot be empty")
        
        pipeline = [
            {"$match": {"userId": user_id}},
            {"$unwind": "$items"},
            {
                "$lookup": {
                    "from": "products",
                    "localField": "items.productId",
                    "foreignField": "_id",
                    "as": "productInfo"
                }
            },
            {"$unwind": "$productInfo"},
            {
                "$group": {
                    "_id": "$_id",
                    "total": {"$sum": {"$multiply": ["$items.qty", "$productInfo.price"]}},
                    "items": {
                        "$push": {
                            "productDetails": {"id": "$productInfo._id", "name": "$productInfo.name"},
                            "qty": "$items.qty"
                        }
                    }
                }
            },
            {"$sort": {"_id": 1}}, # Sort by _id before pagination
            {"$skip": offset},
            {"$limit": limit}
        ]

        cursor = orders_collection.aggregate(pipeline)
        order_list = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            # Convert productDetails.id back to string for response model
            for item in doc["items"]:
                item["productDetails"]["id"] = str(item["productDetails"]["id"])
            order_list.append(models.OrderListDetails(**doc))
        
        next_offset_str = str(offset + limit) if len(order_list) == limit else None
        prev_offset_str = str(offset - limit) if offset > 0 else None

        return {
            "data": order_list,
            "page": {
                "next": next_offset_str,
                "limit": limit,
                "offset": offset,
                "previous": prev_offset_str
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve orders")