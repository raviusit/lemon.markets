# Test API endpoints

#GET http://127.0.0.1:8000/hello
#Accept: application/json

###

#GET http://127.0.0.1:8000/alive
#Accept: application/json

###

#GET http://127.0.0.1:8000/ready
#Accept: application/json


import pytest
from httpx import AsyncClient
from api.main import app  # assuming your FastAPI code is in `main.py`

@pytest.mark.asyncio
async def test_hello():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello!"}

@pytest.mark.asyncio
async def test_ready():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

@pytest.mark.asyncio
async def test_alive():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/alive")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
