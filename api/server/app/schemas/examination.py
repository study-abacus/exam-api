from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

from datetime import datetime

class ExaminationBase(BaseModel):
    name: str
    code: str
    description : str
    exam_start_dt: datetime
    exam_end_dt: datetime

    schema_extra: ClassVar = {
        "example": {
            "name": "Examination Name",
            "code": "EXAM001",
            "description": "XYZ",
            "exam_start_dt": "2021-01-01T00:00:00",
            "exam_end_dt": "2021-01-01T00:00:00"
        }
    }


class ExaminationCreate(ExaminationBase):
    name: str
    code: str
    description : str
    exam_start_dt: datetime
    exam_end_dt: datetime

    schema_extra: ClassVar = {
        "example": {
            "name": "Examination Name",
            "code": "EXAM001",
            "description" : "",
            "exam_start_dt": "2021-01-01T00:00:00",
            "exam_end_dt": "2021-01-01T00:00:00"
        }
    }

class Examination(ExaminationBase):
    id: int
    championship_id: int


    class Config:
        orm_mode = True

class ExaminationAttempts(ExaminationBase):
    id: int
    championship_id: int
    isSubmitted : bool


    class Config:
        orm_mode = True

class ExaminationUpdate(ExaminationBase):
    pass