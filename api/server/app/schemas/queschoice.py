from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

class QuesChoiceBase(BaseModel):
    label: str
    value: str

    schema_extra: ClassVar = {
        "example": {
            "label": "Choice Label",
            "value": "Choice Value"
        }
    }

class QuesChoiceCreate(QuesChoiceBase):
    pass

class QuesChoice(QuesChoiceBase):
    id: int

    class Config:
        orm_mode = True

class QuesChoiceUpdate(QuesChoiceBase):
    pass