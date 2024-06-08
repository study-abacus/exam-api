from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

from datetime import datetime

class ProfileBase(BaseModel):
    name: str
    mothers_name: str
    fathers_name: str
    email: str
    phone: str
    dob: str
    address: str
    city: str
    state: str
    country: str
    pincode: str


    schema_extra: ClassVar = {
        "example": {
            "name": "Profile Name",
            "mothers_name": "Mother Name",
            "fathers_name": "Father Name",
            "email": "abc@gmail.com",
            "phone": "1234567890",
            "dob": "2021-01-01",
            "address": "Address",
            "city": "City",
            "state": "State",
            "country": "Country",
            "pincode": "123456"
        }
    }

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class ProfileUpdate(ProfileBase):
    pass