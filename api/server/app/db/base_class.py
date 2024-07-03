import typing as t

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class_registry: t.Dict = {}




@as_declarative(class_registry=class_registry)
class Base:
    __name__: str

    def as_dict(self):
        return {
            col.name : getattr(self, col.name)
            for col in self.__table__.columns
        }


    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return "sa_"+cls.__name__.lower()
   
 
   
    @declared_attr
    def __table_args__(cls):
        return {"schema": "public"}
   
    @declared_attr
    def __bind_key__(cls) -> str:
        return "public"
    
    @staticmethod
    def foreign_key(column_type, column_name, table_name,  **kwargs):
        return Column(column_type, ForeignKey(f"public.sa_{table_name.lower()}.{column_name}"), **kwargs)








