from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .mixins.created import CreatedMixin
from .mixins.key import IdMixin
from .base import Base


class Question(Base, CreatedMixin, IdMixin):
    __tablename__: str = 'questions'
    text = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at
        }