from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

from datetime import datetime

class ChampionshipBase(BaseModel):
    name: str
    reg_start_dt: datetime
    reg_end_dt: datetime
    primary_price: float = Field(..., description="Primary price", example=100.00, gt=0) #validation for price >0
    secondary_price: float = Field(..., description="Secondary price", example=50.00, gt=0) #validation for price >0
    active: bool = True
    max_exams:int

    @validator('primary_price', 'secondary_price', pre=True)
    def format_price(cls, value):
        return "{:.2f}".format(value)

    schema_extra: ClassVar = {
        "example": {
            "name": "Championship Name",
            "reg_start_dt": "2021-01-01T00:00:00",
            "reg_end_dt": "2021-01-01T00:00:00",
            "primary_price": "100.00",
            "secondary_price": "50.00",
            "active": True
        }
    }

class ChampionshipCreate(ChampionshipBase):
    pass

class Championship(ChampionshipBase):
    id: int

    class Config:
        orm_mode = True

class ChampionshipUpdate(ChampionshipBase):
    pass