from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index ,  Text

from typing import Any

from app.db.base_class import Base
from sqlalchemy.sql import func

class QuestionAttempt(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    answer =  Column(Text)
    admit_card_id = Base.foreign_key(Integer, "id", "AdmitCard")
    question_id = Base.foreign_key(Integer, "id", "Question")
    INS_DT = Column(DateTime(timezone=True), server_default = func.now())
    UPS_DT = Column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now())

    __table_args__ = (
        Index('ix_admit_card_question', 'admit_card_id', 'question_id', unique=True),
    )

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