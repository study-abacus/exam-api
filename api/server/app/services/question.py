from app.utils.app_exceptions import AppException
from app.services.main import AppService, AppCRUD
from app.services.queschoice import QuesChoiceCRUD

from app.utils.service_request import ServiceResult

from app.models.question import Question as QuestionModel
from app.models.question_attempt import QuestionAttempt as QuestionAttemptModel
from app.schemas.question import Question as QuestionSchema
from app.services.ques_attempt import QuestionAttemptCRUD

from sqlalchemy import asc, desc, and_
from sqlalchemy.dialects.postgresql import insert
from typing import List, Any , Optional, Union

import logging
import requests
import json

logger = logging.getLogger(__name__)

class QuestionService(AppService):

    async def get_questions(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve questions.
        """
        try:
            
            result = await QuestionCRUD(self.db).get_all(QuestionModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving questions: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving questions: {str(e)}"}))

    async def create_question(self, examination_id: int, question: QuestionSchema) -> ServiceResult:
        """
        Create new question.
        """
        try:
            result = await QuestionCRUD(self.db).create(QuestionModel,examination_id, question)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating question: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating question: {str(e)}"}))

    async def get_question(self, question_id: int, admit_card_id: int) -> ServiceResult:
        """
        Retrieve question.
        """
        try:
            questions = json.loads(self.cache.hget('questions', question_id) or '{}')
            if not questions:
                questions = await QuestionCRUD(self.db).get(QuestionModel, question_id)
                self.cache.hset('questions', question_id, json.dumps(questions.as_dict() , default= str))
            question_attempt = await QuestionAttemptCRUD(self.db).get(question_id,admit_card_id )
            return ServiceResult({**questions, 'answer' : question_attempt.answer})
        except Exception as e:
            logger.error(f'Error retrieving question: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving question: {str(e)}"}))

    async def answer_question(self, question_id: int, admit_card_id:int, answer: str) -> ServiceResult:
        """
        Update  question.
        """

        try:
            _ = await QuestionAttemptCRUD(self.db).upsert(QuestionAttemptModel, question_id, admit_card_id, answer)
            return await self.get_question(question_id, admit_card_id)
        except Exception as e:
            logger.error(f'Error updating question: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating question: {str(e)}"}))
        
    async def delete_question(self, question_id: int) -> ServiceResult:
        """
        Delete question.
        """
        try:
            result = await QuestionCRUD(self.db).delete(QuestionModel, question_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error deleting question: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting question: {str(e)}"}))

    async def get_examination_questions(self, examination_id: int) -> ServiceResult:
        """
        Retrieve questions for examination.
        """
        try:
            questions = json.loads(self.cache.hget('examination_questions', examination_id) or '{}')
            if not questions:
                questions = await QuestionCRUD(self.db).get_all(QuestionModel, filters=[QuestionModel.examination_id == examination_id])
                self.cache.hset('examination_questions', examination_id, json.dumps([x.as_dict() for x in questions], default= str))
            return ServiceResult(questions)
        except Exception as e:
            logger.error(f'Error retrieving questions for examination: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving questions for examination: {str(e)}"}))


class QuestionCRUD(AppCRUD):

    async def upsert(self, model, id: int, schema: QuestionSchema) -> QuestionModel:
        """
        Upsert question by id.
        """
        try:
            stmt = insert(model).values(id=id, **schema.dict()).on_conflict_do_update(
                index_elements=['id',''],
                set_={field: getattr(schema, field) for field in schema.dict()}
            )
            result = self.db.execute(stmt)
            self.db.commit()
            return self.db.query(model).filter(model.id == id).first()
        except Exception as e:
            self.db.rollback()  # Rollback in case of error
            logger.error(f'Error upserting question: {str(e)}')
            raise AppException.RequestUpdateItem({"ERROR": f"Error upserting question: {str(e)}"})

    async def get_all(self, model, skip: int = 0, limit: int = 100, filters: Optional[List[Any]] = None) -> QuestionModel:
        """
        Retrieve all examinations.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(*filters)
            return query.order_by(asc(model.id)).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f'Error retrieving examinations: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving examinations: {str(e)}"})

    async def create(self, model, examination_id: int, question: QuestionSchema) -> QuestionModel:
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

    async def get(self, model, id: int) -> QuestionModel:
        """
        Retrieve question by id.
        """
        try:
            res =  self.db.query(model ).\
                filter(model.id == id).first()
            return res
        except Exception as e:
            logger.error(f'Error retrieving question: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving question: {str(e)}"})

    async def update(self, model, id: int, schema) -> QuestionModel:
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
        
