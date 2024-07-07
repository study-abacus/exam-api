from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

from datetime import datetime

class QuestionBase(BaseModel):
    questype : str
    title: str
    description: str

    schema_extra: ClassVar = {
        "example": {
            "questype": "Question Type",
            "title": "Question Title",
            "description": "Question Description"
        }
    }

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True

class QuestionUpdate(BaseModel):
    answer : str
    

class QuestionAuth(BaseModel):
    id: int
    title: str
    description: str
    questype: str
    examination_id : int
    answer: Optional[Union[str, None]]

    class Config:
        orm_mode = True
