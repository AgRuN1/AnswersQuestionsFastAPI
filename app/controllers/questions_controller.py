from fastapi import Depends, HTTPException, Query, APIRouter

from app.repositories.answer_repository import AnswerRepository
from app.schemas.question import QuestionSchema
from app.schemas.answer import AnswerSchema
from app.repositories.question_repository import QuestionRepository

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/")
async def get_questions(questionRepository: QuestionRepository=Depends()) -> dict:
    return {
        'data': [question.to_dict() for question in await questionRepository.list()]
    }


@router.post("/")
async def create_question(question: QuestionSchema, questionRepository: QuestionRepository=Depends()) -> dict:
    question = await questionRepository.create(question.text)
    return {
        'result': question.to_dict()
    }


@router.post("/{question_id}/answers")
async def create_answer(
        question_id: int,
        answer: AnswerSchema,
        questionRepository: QuestionRepository=Depends(),
        answerRepository: AnswerRepository = Depends()
) -> dict:
    await questionRepository.get(question_id)
    answer = await answerRepository.create(answer.text, answer.user_id, question_id)
    return {
        'result': answer.to_dict()
    }


@router.get("/{question_id}")
async def get_question(
        question_id: int,
        questionRepository: QuestionRepository=Depends(),
        answerRepository: AnswerRepository = Depends()
) -> dict:
    question = await questionRepository.get(question_id)
    answers = await answerRepository.list_by_question(question_id)
    return {
        'question': question.to_dict(),
        'answers': [answer.to_dict() for answer in answers]
    }


@router.delete("/{question_id}")
async def delete_question(question_id: int, questionRepository: QuestionRepository=Depends()) -> dict:
    await questionRepository.delete(question_id)
    return {
        'result': True
    }