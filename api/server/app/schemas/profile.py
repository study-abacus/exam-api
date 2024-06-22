from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator,  ValidationError
from fastapi import HTTPException
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
    name: Optional[str]
    email: Optional[str]
    country_code : Optional[str]
    phone: Optional[str]

    @validator('phone', pre=True)
    def validate_phone_number(cls, v, values, field):
        country_code = values.get('country_code')
        full_number = f"+{country_code}{v}"

        try:
            parsed_number = phonenumbers.parse(full_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError('Invalid phone number format')
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise ValidationError(f'Invalid phone number: {e}')

        return v


    
class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True

class ProfileUpdate(ProfileBase):
    pass
