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

## 🌐 API Endpoints Summary

Method	Endpoint	Description
POST	/products	Create a new product.
GET	/products	List products with filtering and pagination.
POST	/orders	Create a new order.
GET	/orders/{user_id}	Get a list of orders for a specific user.

For detailed information on request/response bodies, please use the API documentation link above.

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

The application is live and can be accessed at the following URL:

-   **Live API Docs**: **[https://hrone-backend-task-aeh8.onrender.com/docs](https://hrone-backend-task-aeh8.onrender.com/docs)**

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
