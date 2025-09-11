import uuid

from pydantic import BaseModel, field_validator


class AnswerSchema(BaseModel):
    text: str
    user_id: uuid.UUID

    @field_validator('text')
    @classmethod
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError('answer cannot be an empty string')
        return value