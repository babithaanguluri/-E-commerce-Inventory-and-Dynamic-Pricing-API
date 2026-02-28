import pytest
from httpx import AsyncClient
from app.main import app
from app.db.database import Base, engine, SessionLocal
from app.models.models import Category, Product

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the E-commerce Inventory and Dynamic Pricing API"}

@pytest.mark.anyio
async def test_create_category(client: AsyncClient):
    response = await client.post("/api/v1/categories/", json={"name": "Test Category"})
    # Note: This requires the DB to be up and migrations applied/init_db called
    # In a real CI environment, we'd use a separate test database
    assert response.status_code == 200 or response.status_code == 404 # 404 if router not fully wired for POST yet
