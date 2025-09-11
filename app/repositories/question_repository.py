from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy import select

from app.models import Question
from app.repositories.base_repository import AbstractRepository
from app.config.database_helper import get_database_session


class QuestionRepository(AbstractRepository):

    def __init__(self, session=Depends(get_database_session)):
        self.session = session

    async def list(self) -> List[Question]:
        result = await self.session.execute(select(Question))
        return result.scalars().all()

    async def get(self, question_id: int) -> Question:
        question = await self.session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="question not found")
        return question

    async def create(self, text: str) -> Question:
        question = Question(text=text)
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question

    async def delete(self, question_id: int) -> None:
        question = await self.session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="question not found")
        await self.session.delete(question)
        await self.session.commit()