
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Float, Text

from typing import Any

from db.base_class import Base

class Profile(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    name = Column(String(100))
    mothers_name = Column(String(100))
    fathers_name =  Column(String(100))
    email = Column(String(100), nullable = True)
    phone = Column(String(100))
    dob = Column(String(100), nullable = True)
    address = Column(String(100) , nullable = True)
    city = Column(String(100), nullable = True)
    state = Column(String(100), nullable = True)
    pincode = Column(String(100), nullable = True)
    country = Column(String(100), nullable = True)



    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"Profile {self.name}"
    
    def __str__(self) -> str:
        return f"Profiles {self.name}"
    
    def __eq__(self, other):
        return self.name == other.name
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value