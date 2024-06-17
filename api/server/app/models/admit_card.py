from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Float, Text
from sqlalchemy.dialects.postgresql import ARRAY

from typing import Any

from db.base_class import Base

class AdmitCard(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    order_id = Column(Text)
    examination_ids = Column(ARRAY(Integer))
    password_hash = Column(String(100))
    profile_id = Base.foreign_key(Integer, "id", "Profile")
    championship_id = Base.foreign_key(Integer, "id", "Championship")


    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"AdmitCard {self.id}"
    
    def __str__(self) -> str:
        return f"AdmitCard {self.id}"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}