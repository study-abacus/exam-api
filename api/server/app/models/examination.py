from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean ,  Text

from typing import Any

from app.db.base_class import Base

class Examination(Base):
    id = Column(Integer, primary_key = True, nullable = True)
    name = Column(String(100))
    code = Column(String(100))
    description = Column(Text, default = '')
    exam_start_dt = Column(DateTime(timezone=True))
    exam_end_dt = Column(DateTime(timezone=True))
    championship_id = Base.foreign_key(Integer, "id", "Championship")


    def __init__(self, **kwargs) -> None: 
        super().__dict__.update(kwargs)

    def __repr__(self) -> str:
        return f"Examination {self.name}"
    
    def __str__(self) -> str:
        return f"Examination {self.name}"
    
    def __eq__(self, other):
        return self.name == other.name
    
    def add_to_dict(self, key, value):
        self.__dict__[key] = value