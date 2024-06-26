
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Float, Text

from typing import Any

from app.db.base_class import Base

class Profile(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    name = Column(String(100),  nullable = True)
    ci = Column(String(100), nullable = True)
    sa_class =  Column(Integer, nullable = True)
    age =  Column(Integer, nullable= True)
    city = Column(String(100), nullable =True)
    country = Column(String(100), nullable = True)
    guardian_name = Column(String(100), nullable = True)
    email = Column(String(100), nullable = True)
    phone = Column(String(100), nullable = True)

    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"Profile {self.name}"
    
    def __str__(self) -> str:
        return f"Profile {self.name}"
    
    def __eq__(self, other):
        return self.name == other.name
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value