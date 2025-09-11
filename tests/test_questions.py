import pytest


@pytest.mark.asyncio
async def test_questions(test_client):
    response = test_client.get("/questions")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_question(test_client):
    response = test_client.post("/questions", json={'text': 'question'})
    assert response.status_code == 200
    assert response.json()['result']['text'] == 'question'


@pytest.mark.asyncio
async def test_question(test_client):
    response = test_client.get("/questions")
    assert response.status_code == 200
    assert len(response.json()['data']) > 0


