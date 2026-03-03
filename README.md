# E-commerce Inventory and Dynamic Pricing API

A robust, containerized FastAPI application for managing e-commerce inventory with a sophisticated dynamic pricing engine.

## 🌟 Features

- **Inventory Management**: Real-time stock tracking with a thread-safe reservation system (15-minute hold).
- **Dynamic Pricing Engine**: 
  - **Bulk Discounts**: Automatically apply discounts based on quantity (e.g., 10% off for 5+ items).
  - **Seasonal Sales**: Time-based price adjustments for specific categories or site-wide.
  - **BOGO Rules**: "Buy One Get One" logic applied automatically.
  - **User Tiering**: Personalized pricing based on user membership levels.
- **Promotional Campaigns**: Timed marketing campaigns with category-specific targets.
- **Order Processing**: Snapshot records of transactions to ensure historical price accuracy.
- **Inventory Analytics**: Real-time reports for top-selling products and low-stock alerts.
- **Background Tasks**: Automated cleanup of expired reservations using Celery and Redis.
- **Authentication**: Secure OAuth2 JWT-based authentication with role-based access control (ADMIN/USER).

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy 2.0)
- **Task Queue**: Celery + Redis
- **Security**: Passlib (Bcrypt) + Jose (JWT)
- **Infrastructure**: Docker & Docker Compose

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Docker Compose v2+

### Running the Project

1. **Clone and Enter**:
   ```bash
   git clone <your-repository-url>
   cd "E-commerce Inventory and Dynamic Pricing API"
   ```

2. **Launch Services**:
   ```bash
   docker-compose up --build
   ```

3. **Seed the Database** (Required for first run to see sample data):
   ```bash
   docker-compose exec api python -m app.db.seed
   ```

4. **Explore the API**:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📖 API Usage Guide

The repository includes an `api_requests.http` file for the VS Code REST Client.

### Core Workflows:
1.  **Auth**: Register an admin -> Login -> Use the Bearer token for protected routes.
2.  **Inventory**: Add a product variant to your cart to reserve stock.
3.  **Pricing**: Check `GET /api/v1/products/{id}/price?quantity=5` to see dynamic discounts in action.
4.  **Checkout**: Post to `/api/v1/cart/checkout` to finalize the order and decrease stock permanently.

## 🧪 Testing

Run the integration suite within the containerized environment:
```bash
docker-compose exec api pytest tests/integration/test_api.py
```

## ✅ Roadmap

- [x] Phase 1: Core Inventory System (Models, Relationships, Basic CRUD)
- [x] Phase 2: Dynamic Pricing Engine (Bulk, Seasonal, BOGO logic)
- [x] Phase 3: Reservation System & Background Workers (Celery/Redis)
- [x] Phase 4: Orders, Analytics & Promotions
- [x] Phase 5: Authentication & Deployment Ready (JWT, Docker-optimized)

---
*Developed as a high-performance backend solution for modern e-commerce needs.*
