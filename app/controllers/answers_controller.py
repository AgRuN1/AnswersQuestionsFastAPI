from fastapi import Depends, APIRouter

from app.repositories.answer_repository import AnswerRepository

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}")
async def get_answer(answer_id: int, answerRepository: AnswerRepository = Depends()) -> dict:
    answer = await answerRepository.get(answer_id)
    return {
        "result": answer.to_dict()
    }


@router.delete("/{answer_id}")
async def delete_answer(answer_id: int, answerRepository: AnswerRepository = Depends()) -> dict:
    await answerRepository.delete(answer_id)
    return {
        "result": True
    }