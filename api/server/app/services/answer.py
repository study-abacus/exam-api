from app.utils.app_exceptions import AppException
from app.services.main import AppService, AppCRUD

from app.utils.service_request import ServiceResult

from app.models.answer import Answer as AnswerModel
from app.schemas.answer import Answer as AnswerSchema

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

import logging
import requests
import datetime

logger = logging.getLogger(__name__)

class AnswerService(AppService):

    async def get_answers(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve answers.
        """
        try:
            result = await AnswerCRUD(self.db).get_all(AnswerModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving answers: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving answers: {str(e)}"}))

    async def create_answer(self, question_id: int, answer: AnswerSchema) -> ServiceResult:
        """
        Create new answer.
        """
        try:
            result = await AnswerCRUD(self.db).create(AnswerModel,question_id, answer)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating answer: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating answer: {str(e)}"}))

    async def get_answer(self, answer_id: int) -> ServiceResult:
        """
        Retrieve answer.
        """
        try:
            result = await AnswerCRUD(self.db).get(AnswerModel, answer_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving answer: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving answer: {str(e)}"}))

    async def update_answer(self, answer_id: int, answer: AnswerSchema) -> ServiceResult:
        """
        Update answer.
        """
        try:
            result = await AnswerCRUD(self.db).update(AnswerModel, answer_id, answer)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error updating answer: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating answer: {str(e)}"}))

    async def delete_answer(self, answer_id: int) -> ServiceResult:
        """
        Delete answer.
        """
        try:
            result = await AnswerCRUD(self.db).delete(AnswerModel, answer_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error deleting answer: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting answer: {str(e)}"}))

    async  def get_answers_by_question_id(self, question_id: int) -> ServiceResult:
        """
        Retrieve answers by question_id.
        """
        try:
            result = await AnswerCRUD(self.db).get_all(AnswerModel, filters=[AnswerModel.question_id == question_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving answers: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving answers: {str(e)}"}))

    async def get_question_answers(self, question_id: int) -> ServiceResult:
        """
        Retrieve question answers.
        """
        try:
            result = await AnswerCRUD(self.db).get_all(AnswerModel, filters=[AnswerModel.question_id == question_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving answers: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving answers: {str(e)}"}))

class AnswerCRUD(AppCRUD):

    async def get_all(self, model, skip: int = 0, limit: int = 100, filters: Optional[List[Any]] = None) -> AnswerModel:
        """
        Retrieve all answers.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(*filters)
            return query.order_by(asc(model.id)).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f'Error retrieving answers: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving answers: {str(e)}"}))

    async def create(self, model, question_id: int, answer) -> AnswerModel:
        """
        Create new answer.
        """

        try:
            answer = model(**answer.dict(), question_id=question_id)
            self.db.add(answer)
            self.db.commit()
            self.db.refresh(answer)
            return answer

        except Exception as e:
            logger.error(f'Error creating answer: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating answer: {str(e)}"}))

    async def get(self, model, answer_id: int) -> AnswerModel:
        """
        Retrieve answer.
        """
        try:
            return self.db.query(model).filter(model.id == answer_id).first()
        except Exception as e:
            logger.error(f'Error retrieving answer: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving answer: {str(e)}"}))

    async def update(self, model, id: int, schema) -> AnswerModel:
        """
        Update answer.
        """
        try:
            # Get the existing record
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
            logger.error(f'Error updating answer: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating answer: {str(e)}"}))

    async def delete(self, model, answer_id: int) -> AnswerModel:
        """
        Delete answer.
        """
        try:
            answer = self.db.query(model).filter(model.id == answer_id).first()
            if not answer:
                raise ValueError(f'Answer not found for id: {answer_id}')

            self.db.delete(answer)
            self.db.commit()
            return answer

        except Exception as e:
            logger.error(f'Error deleting answer: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting answer: {str(e)}"}))
