from pydantic import BaseModel , Field , validator
from typing import List, Any , Optional, Union, ClassVar

class AdmitCardBase(BaseModel):
    order_id: str

    schema_extra: ClassVar = {
        "example": {
            "order_id": 1
        }
    }

class AdmitCardCreate(AdmitCardBase):
    pass

class AdmitCard(AdmitCardBase):
    id: int
    examination_ids : List[int]
    profile_id : int
    championship_id : int

    class Config:
        orm_mode = True

class AdmitCardUpdate(AdmitCardBase):
    pass