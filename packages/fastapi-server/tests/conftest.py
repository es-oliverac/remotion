"""Pytest configuration"""
import pytest
import asyncio
from httpx import AsyncClient
from app.main import app
from app.services.queue import RenderQueue


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def clean_queue():
    """Clean up queue before tests"""
    from app.services.queue import queue
    test_queue = RenderQueue(max_concurrent=1)
    await test_queue.start()
    yield test_queue
    await test_queue.stop()
