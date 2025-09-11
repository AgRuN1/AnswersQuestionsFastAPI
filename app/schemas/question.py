from pydantic import BaseModel, field_validator


class QuestionSchema(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError('question cannot be an empty string')
        return value