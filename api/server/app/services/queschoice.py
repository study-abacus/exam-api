from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from utils.service_request import ServiceResult

from models.queschoice import QuesChoice as QuesChoiceModel
from schemas.queschoice import QuesChoice as QuesChoiceSchema

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

import logging
import requests
import datetime

logger = logging.getLogger(__name__)

class QuesChoiceService(AppService):
    
    async def get_queschoices(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve queschoices.
        """
        try:
            result = await QuesChoiceCRUD(self.db).get_all(QuesChoiceModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving queschoices: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving queschoices: {str(e)}"}))

    async def create_queschoice(self, question_id: int, queschoice: QuesChoiceSchema) -> ServiceResult:
        """
        Create new queschoice.
        """
        try:
            result = await QuesChoiceCRUD(self.db).create(QuesChoiceModel,question_id, queschoice)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating queschoice: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating queschoice: {str(e)}"}))

    async def get_queschoice(self, queschoice_id: int) -> ServiceResult:
        """
        Retrieve queschoice.
        """
        try:
            result = await QuesChoiceCRUD(self.db).get(QuesChoiceModel, queschoice_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving queschoice: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving queschoice: {str(e)}"}))
    
    async def update_queschoice(self, queschoice_id: int, queschoice: QuesChoiceSchema) -> ServiceResult:
        """
        Update queschoice.
        """
        try:
            result = await QuesChoiceCRUD(self.db).update(QuesChoiceModel, queschoice_id, queschoice)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error updating queschoice: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating queschoice: {str(e)}"}))

    async def delete_queschoice(self, queschoice_id: int) -> ServiceResult:
        """
        Delete queschoice.
        """
        try:
            result = await QuesChoiceCRUD(self.db).delete(QuesChoiceModel, queschoice_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error deleting queschoice: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting queschoice: {str(e)}"}))

    async def get_queschoices_by_question(self, question_id: int) -> ServiceResult:
        """
        Retrieve queschoices for question.
        """
        try:
            result = await QuesChoiceCRUD(self.db).get_all(QuesChoiceModel, filters=[QuesChoiceModel.question_id == question_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving queschoices for question: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving queschoices for question: {str(e)}"}))

class QuesChoiceCRUD(AppCRUD):

    async def get_all(self, model, skip: int = 0, limit: int = 100, filters: Optional[List[Any]] = None):
        """
        Retrieve all queschoices.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(*filters)
            return  query.order_by(asc(model.id)).offset(skip).limit(limit).all()

        except Exception as e:
            logger.error(f'Error retrieving queschoices: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving queschoices: {str(e)}"})


    async def create(self, model, question_id: int, schema: QuesChoiceSchema):
        """
        Create new queschoice.
        """
        try:
            new_queschoice = model(**schema.dict(), question_id=question_id)
            self.db.add(new_queschoice)
            self.db.commit()
            self.db.refresh(new_queschoice)
            return new_queschoice
        except Exception as e:
            logger.error(f'Error creating queschoice: {str(e)}')
            return AppException.RequestCreateItem( {"ERROR": f"Error creating queschoice: {str(e)}"})   

    async def get(self, model, queschoice_id: int):
        """
        Retrieve queschoice.
        """
        try:
            return  self.db.query(model).filter(model.id == queschoice_id).first()
        except Exception as e:
            logger.error(f'Error retrieving queschoice: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving queschoice: {str(e)}"})

    async def update(self, model, queschoice_id: int, schema: QuesChoiceSchema):
        """
        Update queschoice.
        """
        try:
            queschoice =  self.db.query(model).filter(model.id == queschoice_id).first()
            for key, value in schema.dict().items():
                setattr(queschoice, key, value)
            self.db.commit()
            self.db.refresh(queschoice)
            return queschoice
        except Exception as e:
            logger.error(f'Error updating queschoice: {str(e)}')
            return AppException.RequestUpdateItem( {"ERROR": f"Error updating queschoice: {str(e)}"})

    async def delete(self, model, queschoice_id: int):
        """
        Delete queschoice.
        """
        try:
            queschoice =  self.db.query(model).filter(model.id == queschoice_id).first()
            self.db.delete(queschoice)
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f'Error deleting queschoice: {str(e)}')
            return AppException.RequestDeleteItem( {"ERROR": f"Error deleting queschoice: {str(e)}"})