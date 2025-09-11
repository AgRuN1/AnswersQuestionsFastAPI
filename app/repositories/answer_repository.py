import uuid
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select

from app.models import Answer
from app.repositories.base_repository import AbstractRepository
from app.config.database_helper import get_database_session


class AnswerRepository(AbstractRepository):

    def __init__(self, session=Depends(get_database_session)):
        self.session = session

    async def list_by_question(self, question_id: int) -> List[Answer]:
        result = await self.session.execute(select(Answer).where(Answer.question_id == question_id))
        return result.scalars().all()

    async def get(self, answer_id: int) -> Answer:
        answer = await self.session.get(Answer, answer_id)
        if not answer:
            raise HTTPException(status_code=404, detail="answer not found")
        return answer

    async def create(self, text: str, user_id: uuid.UUID, question_id: int) -> Answer:
        answer = Answer(text=text, user_id=user_id, question_id=question_id)
        self.session.add(answer)
        await self.session.commit()
        await self.session.refresh(answer)
        return answer

    async def delete(self, answer_id: int) -> None:
        answer = await self.session.get(Answer, answer_id)
        if not answer:
            raise HTTPException(status_code=404, detail="answer not found")
        await self.session.delete(answer)
        await self.session.commit()