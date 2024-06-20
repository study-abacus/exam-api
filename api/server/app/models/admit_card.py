from sqlalchemy import Column, Integer, String, Text, Sequence
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.base_class import Base

admit_card_id_seq = Sequence('admit_card_id_seq', start=1000, increment=1)

class AdmitCard(Base):
    id = Column(Integer, admit_card_id_seq, primary_key=True, nullable=False, server_default=admit_card_id_seq.next_value())
    order_id = Column(Text, nullable=True)
    examination_ids = Column(ARRAY(Integer), nullable=True)
    password_hash = Column(String(100), nullable=True)
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
