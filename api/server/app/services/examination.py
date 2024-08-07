from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.utils.service_request import ServiceResult

from app.models.examination import Examination as ExaminationModel
from app.schemas.examination import Examination as ExaminationSchema
from app.services.exam_attempt import ExamAttemptCRUD 

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

import logging
import requests
import json

logger = logging.getLogger(__name__)

class ExaminationService(AppService):

    async def get_examinations(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve examinations.
        """
        try:
            result = await ExaminationCRUD(self.db).get_all(ExaminationModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving examinations: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving examinations: {str(e)}"}))

    async def create_examination(self, championship_id: int, examination: ExaminationSchema) -> ServiceResult:
        """
        Create new examination.
        """
        try:
            result = await ExaminationCRUD(self.db).create(ExaminationModel,championship_id, examination)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating examination: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating examination: {str(e)}"}))

    async def get_examination(self, examination_id: int, admit_card_id:int ) -> ServiceResult:
        """
        Retrieve examination.
        """
        try:
            examination = (await ExaminationCRUD(self.db, self.cache).get( examination_id)).as_dict()
            exam_attempt = await ExamAttemptCRUD(self.db, self.cache).get(examination_id, admit_card_id)
            examination['is_submitted'] = exam_attempt.is_submitted if exam_attempt else False
            return ServiceResult(examination)
        except Exception as e:
            logger.error(f'Error retrieving examination: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving examination: {str(e)}"}))

    async def update_examination(self, examination_id: int, examination: ExaminationSchema) -> ServiceResult:
        """
        Update examination.
        """
        try:
            result = await ExaminationCRUD(self.db).update(ExaminationModel, examination_id, examination)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error updating examination: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating examination: {str(e)}"}))

    async def delete_examination(self, examination_id: int) -> ServiceResult:
        """
        Delete examination.
        """
        try:
            result = await ExaminationCRUD(self.db).delete(ExaminationModel, examination_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error deleting examination: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting examination: {str(e)}"}))

    async def get_championship_examinations(self, championship_id: int,  skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve examinations for championship.
        """
        try:
            result = await ExaminationCRUD(self.db).get_all(  skip, limit,filters=[ExaminationModel.championship_id == championship_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving championship examinations: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving championship examinations: {str(e)}"}))

class ExaminationCRUD(AppCRUD):

    async def get_all(self,  skip: int = 0, limit: int = 100,model=ExaminationModel, filters: Optional[List[Any]] = None) -> ExaminationModel:
        """
        Retrieve all examinations.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(*filters)
            return query.order_by(asc(model.name)).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f'Error retrieving examinations: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving examinations: {str(e)}"})

    async def create(self, model, championship_id: int, examination: ExaminationSchema) -> ExaminationModel:
        """
        Create new examination.
        """
        try:
            examination = model(**examination.dict(), championship_id=championship_id)
            self.db.add(examination)
            self.db.commit()
            self.db.refresh(examination)
            return examination
        except Exception as e:
            logger.error(f'Error creating examination: {str(e)}')
            return AppException.RequestCreateItem( {"ERROR": f"Error creating examination: {str(e)}"})

    async def get(self,  id: int,model= ExaminationModel) -> ExaminationModel:
        """
        Retrieve examination by id.
        """
        try:
            exam_details = json.loads(self.cache.hget('examiantions', id) or '{}')
            if not exam_details:
                exam_details =  self.db.query(model).filter(model.id == id).first()
                self.cache.hset('examinations', id, json.dumps(exam_details.as_dict(), default=str))
            return exam_details
        except Exception as e:
            logger.error(f'Error retrieving examination: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving examination: {str(e)}"})

    async def update(self, model, id: int, schema) -> ExaminationModel:
        """
        Update examination by id.
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
            return AppException.RequestUpdateItem( {"ERROR": f"Error updating championship: {str(e)}"})

    async def delete(self, model, id: int) -> ExaminationModel:
        """
        Delete examination by id.
        """
        try:
            record = self.db.query(model).filter(model.id == id).first()
            if not record:
                raise ValueError("Record not found")
            self.db.delete(record)
            self.db.commit()
            return record
        except Exception as e:
            logger.error(f'Error deleting examination: {str(e)}')
            return AppException.RequestDeleteItem( {"ERROR": f"Error deleting examination: {str(e)}"})
