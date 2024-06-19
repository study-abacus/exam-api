from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Float, Text

from typing import Any

from app.db.base_class import Base

class QuesChoice(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    label = Column(Text)
    value = Column(Text)
    question_id = Base.foreign_key(Integer, "id", "Question")


    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"QuesChoice {self.name}"
    
    def __str__(self) -> str:
        return f"QuesChoice {self.name}"
    
    def __eq__(self, other):
        return self.name == other.name
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value