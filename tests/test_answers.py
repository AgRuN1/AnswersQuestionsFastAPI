import pytest


@pytest.mark.asyncio
async def test_answer(test_client):
    response = test_client.get("/answers/1")
    assert response.status_code == 404
