from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator,  ValidationError
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
            return None  # If phone is None, validation pass (assuming it's optional)

        country_code = values.get('country_code')
        if country_code is None:
            raise ValidationError('Country code is required if phone number is provided')

        full_number = f"+{country_code}{v}"

        try:
            parsed_number = phonenumbers.parse(full_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValueError('Invalid phone number format')
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise AppException.RequestOrderCreateItem( {"ERROR": f"Please Check Your Details"})

        return v
    


    
class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class ProfileUpdate(ProfileBase):
    pass
