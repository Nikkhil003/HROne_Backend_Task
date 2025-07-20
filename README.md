# HROne E-commerce Backend API

A FastAPI-based e-commerce backend application.

## 🚀 Features

- **Product Management**: Create and list products with sizes and quantities
- **Order Management**: Create orders and retrieve user order history
- **Advanced Filtering**: Search products by name and filter by size
- **Pagination**: Efficient pagination for large datasets
- **Data Validation**: Comprehensive input validation and error handling
- **MongoDB Integration**: Async MongoDB operations using Motor

## 🛠 Tech Stack

- **Framework**: FastAPI 
- **Database**: MongoDB (MongoDB Atlas M0)
- **ODM**: Motor (Async MongoDB driver)
- **Validation**: Pydantic
- **Server**: Uvicorn

## 📁 Project Structure

```
HROne_Backend_task/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models for request/response
│   ├── database.py          # MongoDB connection setup
│   └── routers/
│       ├── __init__.py
│       ├── products.py      # Product-related endpoints
│       └── orders.py        # Order-related endpoints
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd HROne_Backend_task
```

### 2. Create virtual environment
```bash
conda create -p venv python==3.12
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```env
MONGO_URI="your_mongodb_atlas_connection_string"
SECRET_KEY=your-secret-key
```

### 5. Run the application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🌐 API Endpoints

### Products

#### Create Product
- **POST** `/products`
- **Request Body**:
```json
{
  "name": "Product Name",
  "price": 29.99,
  "sizes": [
    {"size": "small", "quantity": 10},
    {"size": "medium", "quantity": 15},
    {"size": "large", "quantity": 8}
  ]
}
```
- **Response**: `201 Created`
```json
{
  "id": "product_id_string"
}
```

#### List Products
- **GET** `/products`
- **Query Parameters** (all optional):
  - `name`: Filter by product name (partial search supported)
  - `size`: Filter by available size (e.g., "large")
  - `limit`: Number of products to return (default: 10, max: 100)
  - `offset`: Number of products to skip for pagination (default: 0)
- **Response**: `200 OK`
```json
{
  "data": [
    {
      "id": "product_id",
      "name": "Product Name",
      "price": 29.99
    }
  ],
  "page": {
    "next": "20",
    "limit": 10,
    "offset": 0,
    "previous": null
  }
}
```

### Orders

#### Create Order
- **POST** `/orders`
- **Request Body**:
```json
{
  "userId": "user123",
  "items": [
    {
      "productId": "product_id_string",
      "qty": 2
    }
  ]
}
```
- **Response**: `201 Created`
```json
{
  "id": "order_id_string"
}
```

#### Get User Orders
- **GET** `/orders/{user_id}`
- **Path Parameters**:
  - `user_id`: The ID of the user
- **Query Parameters** (optional):
  - `limit`: Number of orders to return (default: 10, max: 100)
  - `offset`: Number of orders to skip for pagination (default: 0)
- **Response**: `200 OK`
```json
{
  "data": [
    {
      "id": "order_id",
      "items": [
        {
          "productDetails": {
            "id": "product_id",
            "name": "Product Name"
          },
          "qty": 2
        }
      ],
      "total": 59.98
    }
  ],
  "page": {
    "next": "20",
    "limit": 10,
    "offset": 0,
    "previous": null
  }
}
```

## 🗄 Database Schema

### Products Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "price": "number",
  "sizes": [
    {
      "size": "string",
      "quantity": "number"
    }
  ]
}
```

### Orders Collection
```json
{
  "_id": "ObjectId",
  "userId": "string",
  "items": [
    {
      "productId": "ObjectId",
      "qty": "number"
    }
  ]
}
```

## 🔍 Key Features

### Data Validation
- Comprehensive input validation using Pydantic models
- Business logic validation (positive prices, quantities, etc.)
- MongoDB ObjectId validation for product references

### Error Handling
- Structured error responses
- Proper HTTP status codes
- Detailed error messages for debugging

### Performance Optimizations
- Efficient MongoDB queries with proper indexing considerations
- Pagination to handle large datasets
- Selective field projection for list endpoints

### Security Considerations
- Input sanitization to prevent injection attacks
- Regex escaping for search functionality
- Rate limiting through query parameter constraints

## 🧪 Testing

### Manual Testing with cURL

Create a product:
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sample T-Shirt",
    "price": 25.99,
    "sizes": [
      {"size": "small", "quantity": 10},
      {"size": "medium", "quantity": 15},
      {"size": "large", "quantity": 8}
    ]
  }'
```

List products:
```bash
curl "http://localhost:8000/products?limit=5&offset=0"
```

### Using Swagger UI
Visit http://localhost:8000/docs for interactive API testing.

## 🚀 Deployment

The application is configured for deployment on platforms like Render or Railway:

1. **Environment Variables**: Set `MONGO_URI` in your deployment platform
2. **Host Configuration**: Application binds to `0.0.0.0:8000`
3. **Dependencies**: All listed in `requirements.txt`

## 👨‍💻 Development

### Code Quality
- Clean, readable code with comprehensive documentation
- Proper error handling and logging
- Modular structure with separation of concerns
- Type hints throughout the codebase

### MongoDB Optimization
- Efficient aggregation pipelines for complex queries
- Proper indexing strategy (recommended: index on `userId` for orders)
- Optimized field projections to reduce data transfer

## 📝 License

This project is created for the HROne Backend Intern Hiring Task.

## 🤝 Contact

For any questions regarding this implementation, please refer to the task submission guidelines.
