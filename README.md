# E-commerce Inventory and Dynamic Pricing API

A robust, containerized FastAPI application for managing e-commerce inventory with a flexible dynamic pricing engine.

## Features

- **Inventory Management**: Real-time stock tracking and reservation system.
- **Dynamic Pricing Engine**: 
  - **Bulk Discounts**: Automatically apply discounts based on quantity.
  - **Seasonal Sales**: Time-based price adjustments.
  - **User Tiering**: (Upcoming) Personalized pricing.
- **Promotional Campaigns**: Site-wide or category-specific marketing campaigns.
- **Order Tracking**: Permanent record of all transactions and snapshot prices.
- **Inventory Analytics**: Low-stock alerts and reports.
- **Background Tasks**: Automated cleanup of expired reservations using Celery/Redis.
- **Containerized**: Fully Dockerized for easy deployment (FastAPI, PostgreSQL, Redis, Celery).

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **Task Queue**: Celery + Redis
- **Validation**: Pydantic v2
- **Infrastructure**: Docker & Docker Compose

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- Docker Compose

### Running the Project

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd "E-commerce Inventory and Dynamic Pricing API"
   ```

2. **Launch with Docker**:
   ```bash
   docker-compose up --build
   ```

3. **Access API Documentation**:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Usage Examples

The repository includes an `api_requests.http` file for VS Code REST Client, containing structured requests for:
- Creating Products/Categories
- Managing Inventory
- Adding Pricing Rules
- Running Promotions
- Checking out Carts

## Testing

Run integration tests using Docker:
```bash
docker-compose exec api pytest
```

## Roadmap

- [x] Phase 1: Core Inventory System
- [x] Phase 2: Dynamic Pricing Rules
- [x] Phase 3: Orders & Analytics
- [x] Phase 4: Search & Promotions
- [ ] Phase 5: Authentication & Authorization (Complete)
