from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Text

from typing import Any

from app.db.base_class import Base

class QuestionAttempt(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    answer =  Column(Text)
    admit_card_id = Base.foreign_key(Integer, "id", "AdmitCard")
    question_id = Base.foreign_key(Integer, "id", "Question")
    INS_DT = Column(DateTime)
    UPS_DT = Column(DateTime)

    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"Question Attempt {self.answer} {self.id}"
    
    def __str__(self) -> str:
        return f"Question Attempt {self.answer} {self.id}"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value