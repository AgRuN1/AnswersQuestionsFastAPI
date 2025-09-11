from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .mixins.created import CreatedMixin
from .mixins.key import IdMixin
from .base import Base


class Answer(Base, CreatedMixin, IdMixin):
    __tablename__: str = 'answers'
    text = Column(String, nullable=False)
    user_id = Column(UUID(), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at
        }