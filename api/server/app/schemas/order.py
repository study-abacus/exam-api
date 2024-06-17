from typing import List, Any , Optional, Union, ClassVar
from pydantic import BaseModel, validator, Field

class OrderBase(BaseModel):
    amount : float = Field(..., description="Amount", example=100.00, gt=0) #validation for price >0
    currency : str = Field(..., description="Currency", example="USD")
    order_id : str = Field(..., description="Order ID", example="order_123")

class OrderCreate(BaseModel):
    championship_id: int
    examination_ids : List[int]

class OrderAmount(BaseModel):
    amount : float
    notes : str

class OrderCapture(BaseModel):
    payment_id : str
    signature : str