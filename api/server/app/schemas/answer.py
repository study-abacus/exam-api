from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

class AnswerBase(BaseModel):
    value: str

    schema_extra: ClassVar = {
        "example": {
            "value": "Answer Value"
        }
    }

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True

class AnswerUpdate(AnswerBase):
    pass
