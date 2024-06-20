from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Float
from sqlalchemy.dialects.mysql import FLOAT

from typing import Any

from app.db.base_class import Base

class Championship(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    name = Column(String(100))
    reg_start_dt = Column(DateTime)
    reg_end_dt = Column(DateTime)
    primary_price = Column(FLOAT(precision=10, scale=2))
    secondary_price = Column(FLOAT(precision=10, scale=2))
    active = Column(Boolean)
    max_exams =  Column(Integer, nullable =  True)


    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"Championship {self.name}"
    
    def __str__(self) -> str:
        return f"Championship {self.name}"
    
    def __eq__(self, other):
        return self.name == other.name
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value