from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

from datetime import datetime

class ProfileBase(BaseModel):
    name: Optional[str]
    ci : Optional[str]
    guardian_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]



    
class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class ProfileUpdate(ProfileBase):
    pass
