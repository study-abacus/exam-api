from app.utils.app_exceptions import AppException
from app.services.main import AppService, AppCRUD

from app.utils.service_request import ServiceResult

from app.models.question import Question as QuestionModel
from app.models.question_attempt import QuestionAttempt as QuestionAttemptModel
from app.schemas.question import Question as QuestionSchema

from sqlalchemy import asc, desc, and_
from sqlalchemy.dialects.postgresql import insert
from typing import List, Any , Optional, Union

import logging
import requests
import json

logger = logging.getLogger(__name__)


class QuestionAttemptCRUD(AppCRUD):

    async def upsert(self, model, question_id:int, admit_card_id:int, answer:str) -> QuestionAttemptModel:
        """
        Upsert question by id.
        """
        try:
            values_to_insert = {
                'admit_card_id' : admit_card_id,
                'question_id' : question_id,
                'answer' : answer
            }
            values_to_update = {
                'answer' : answer
            }
            stmt = insert(model).values(**values_to_insert).on_conflict_do_update(
                index_elements=['admit_card_id','question_id'],
                set_=values_to_update
            )
            result = self.db.execute(stmt)
            self.db.commit()
            return self.db.query(model).filter(and_(model.admit_card_id == admit_card_id, model.question_id ==  question_id)).first()
        except Exception as e:
            self.db.rollback()  # Rollback in case of error
            logger.error(f'Error upserting question: {str(e)}')
            raise AppException.RequestUpdateItem({"ERROR": f"Error upserting question: {str(e)}"})

    async def get_all(self, skip: int = 0, limit: int = 100, filters: Optional[List[Any]] = None, model = QuestionAttemptModel) -> QuestionAttemptModel:
        """
        Retrieve all examinations.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(*filters)
            return query.order_by(asc(model.id)).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f'Error retrieving Question Attempts: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving question attempts: {str(e)}"})

    async def create(self, model, examination_id: int, question: QuestionSchema) -> QuestionAttemptModel:
        """
        Create new question.
        """
        try:
            question = model(examination_id=examination_id, **question.dict())
            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            return question
        except Exception as e:
            logger.error(f'Error creating question: {str(e)}')
            return AppException.RequestCreateItem( {"ERROR": f"Error creating question: {str(e)}"})

    async def get(self,  question_id: int, admit_card_id:int,model= QuestionAttemptModel ) -> QuestionAttemptModel:
        """
        Retrieve question by id.
        """
        try:
            res =  self.db.query(model).filter(and_(model.question_id == question_id, model.admit_card_id == admit_card_id)).first()
            # print(f'res {res}')
            return res
        except Exception as e:
            logger.error(f'Error retrieving question: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving question: {str(e)}"})

    async def update(self, model, id: int, schema) -> QuestionAttemptModel:
        """
        Update question by id.
        """
        try:
            record = self.db.query(model).filter(model.id == id).first()
            if not record:
                raise ValueError("Record not found")

            # Update the record with the new values
            for field, value in schema.dict().items():
                if hasattr(record, field):
                    setattr(record, field, value)

            self.db.commit()
            self.db.refresh(record)
            return record
        except Exception as e:
            logger.error(f'Error updating question: {str(e)}')
            return AppException.RequestUpdateItem( {"ERROR": f"Error updating question: {str(e)}"})

    async def delete(self, model, id: int) -> bool:
        """
        Delete question by id.
        """
        try:
            question = self.db.query(model).filter(model.id == id).first()
            self.db.delete(question)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error deleting question: {str(e)}')
            return AppException.RequestDeleteItem( {"ERROR": f"Error deleting question: {str(e)}"})
        
