from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator,  root_validator
from fastapi import HTTPException
from app.utils.app_exceptions  import AppException
from datetime import datetime
import phonenumbers

class ProfileBase(BaseModel):
    name: Optional[str]
    ci : Optional[str]
    sa_class : Optional[int]
    city : Optional[str]
    country : Optional[str]
    age : Optional[int]
    guardian_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]


class ProfileOrderCreate(BaseModel):
    name: Optional[str] =None
    email: Optional[str] =None
    country_code : Optional[str] =None
    phone: Optional[str] =None

    @validator('phone', pre=True)
    def validate_phone_number(cls, v, values, field):
        if v is None:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})

        country_code = values.get('country_code')
        if country_code is None:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})

        # Check if the phone number has exactly 10 digits
        if len(v) != 10:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})

        full_number = f"+{country_code}{v}"

        try:
            parsed_number = phonenumbers.parse(full_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})
        except phonenumbers.phonenumberutil.NumberParseException:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})

        return v
    
    @validator('email', pre=True)
    def validate_email(cls,v, values, field):
        if v is None:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})
        if len(v) == 0:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})
        
        return v
    
    @validator('name', pre=True)
    def validate_name(cls,v, values, field):
        if v is None:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})
        if len(v) == 0:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})
        
        return v

    @root_validator
    def check_name_or_email(cls, values):
        name = values.get('name')
        email = values.get('email')
        if not name and not email:
            raise AppException.RequestOrderCreateItem({"ERROR": "Please Check Your Details"})
        return values
    


    
class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class ProfileUpdate(ProfileBase):
    pass
