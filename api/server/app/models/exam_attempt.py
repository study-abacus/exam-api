from sqlalchemy import Column, Integer,  Boolean, DateTime, Index

from typing import Any

from app.db.base_class import Base
from sqlalchemy.sql import func

class ExamAttempt(Base):
    id  = Column(Integer, primary_key = True, nullable = True)
    is_submitted = Column(Boolean)
    admit_card_id = Base.foreign_key(Integer, "id", "AdmitCard")
    examination_id = Base.foreign_key(Integer, "id", "Examination")
    INS_DT = Column(DateTime(timezone=True))
    END_DT = Column(DateTime(timezone=True), nullable = True)

    __table_args__ = (
        Index('ix_admit_card_examination', 'admit_card_id', 'examination_id', unique=True),
    )

    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"Examination Attempt {self.is_submitted} {self.id}"
    
    def __str__(self) -> str:
        return f"Examination Attempt {self.is_submitted} {self.id}"
    
    def __eq__(self, other):
        return self.id == other.id
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value
