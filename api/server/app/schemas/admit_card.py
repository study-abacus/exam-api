from pydantic import BaseModel , Field , validator
from typing import List, Any , Optional, Union, ClassVar

class AdmitCardBase(BaseModel):
    order_id: str
    password : Optional[str]
    examination_ids : List[int]
    championship_id : int
    


    
class AdmitCardCreate(AdmitCardBase):
    pass

class AdmitCard(AdmitCardBase):
    id: int
    profile_id: int
    

    class Config:
        orm_mode = True

class AdmitCardUpdate(AdmitCardBase):
    pass
