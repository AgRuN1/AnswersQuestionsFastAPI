import pytest

class TestQuestions:
    question = 'Сколько в мире океанов ?'
    answer1 = 'В мире 6 океанов'
    answer2 = 'В мире 5 океанов'

    @pytest.mark.asyncio
    async def test_questions(self, test_client):
        response = test_client.get("/questions")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_create_question(self, test_client):
        response = test_client.post("/questions", json={'text': self.question})
        assert response.status_code == 200
        assert response.json()['result']['text'] == self.question

    @pytest.mark.asyncio
    async def test_create_question_no_text(self, test_client):
        response = test_client.post("/questions", json={'text': ''})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_question(self, test_client):
        response = test_client.get("/questions")
        assert response.status_code == 200
        result = response.json()
        assert len(result['data']) > 0
        assert result['data'][0]['text'] == self.question
        assert result['data'][0]['id'] == 1

    @pytest.mark.asyncio
    async def test_answer(self, test_client):
        response = test_client.get("/answers/1")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_answer(self, test_client):
        data = {
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "text": self.answer1,
        }
        response = test_client.post("/questions/1/answers", json=data)
        assert response.status_code == 200
        assert response.json()['result']['text'] == data['text']
        assert response.json()['result']['user_id'] == data['user_id']
        data['text'] = ''
        response = test_client.post("/questions/1/answers", json=data)
        assert response.status_code == 422
        data['text'] = self.answer2
        response = test_client.post("/questions/1/answers", json=data)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_question_with_answers(self, test_client):
        response = test_client.get("/questions/1")
        assert response.status_code == 200
        data = response.json()
        question = data['question']
        answers = data['answers']
        assert question['text'] == self.question
        assert len(answers) == 2
        assert answers[0]['text'] == self.answer1
        assert answers[1]['text'] == self.answer2

    @pytest.mark.asyncio
    async def test_delete_answer(self, test_client):
        response = test_client.get("/answers/2")
        assert response.status_code == 200
        assert response.json()['result']['text'] == self.answer2

        response = test_client.delete("/answers/2")
        assert response.status_code == 200
        assert response.json()['result'] == True

        response = test_client.delete("/answers/2")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_question(self, test_client):
        response = test_client.delete("/questions/1")
        assert response.status_code == 200
        assert response.json()['result'] == True

        response = test_client.get("/questions/1")
        assert response.status_code == 404