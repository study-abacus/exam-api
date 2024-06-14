from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from utils.service_request import ServiceResult

from models.championship import Championship as ChampionshipModel
from schemas.championship import Championship as ChampionshipSchema

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

import logging
import requests
import datetime

logger = logging.getLogger(__name__)


class ChampionshipService(AppService):
    
    async def get_championships(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve championships.
        """
        try:
            result = await ChampionshipCRUD(self.db).get_all(ChampionshipModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving championships: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving championships: {str(e)}"}))

    async def create_championship(self,  championship: ChampionshipSchema) -> ServiceResult:
        """
        Create new championship.
        """
        try:
            result = await ChampionshipCRUD(self.db).create(ChampionshipModel, championship)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating championship: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating championship: {str(e)}"}))

    async def get_championship(self, championship_id: int) -> ServiceResult:
        """
        Retrieve championship.
        """
        try:
            result = await ChampionshipCRUD(self.db).get(ChampionshipModel, championship_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving championship: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving championship: {str(e)}"}))

    async def update_championship(self, championship_id: int, championship: ChampionshipSchema) -> ServiceResult:
        """
        Update championship.
        """
        try:
            result = await ChampionshipCRUD(self.db).update(ChampionshipModel, championship_id, championship)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error updating championship: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating championship: {str(e)}"}))
    
    async def delete_championship(self, championship_id: int) -> ServiceResult:
        """
        Delete championship.
        """
        try:
            result = await ChampionshipCRUD(self.db).delete(ChampionshipModel, championship_id)
            return ServiceResult(True)
        except Exception as e:
            logger.error(f'Error deleting championship: {str(e)}')
            return ServiceResult(False)

class ChampionshipCRUD(AppCRUD):

    async def get_all(self, model, skip: int = 0, limit: int = 100) -> ChampionshipModel:
        """
        Retrieve all records.
        """
        try:
            # Get all records
            result =  self.db.query(model).offset(skip).limit(limit).all()
            return result
        except Exception as e:
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving championships: {str(e)}"})

    async def create(self, model, schema) -> ChampionshipModel:
        """
        Create new record.
        """
        try:
            result = model(**schema.dict())
            self.db.add(result)
            self.db.commit()
            self.db.refresh(result)
            return result
        except Exception as e:
            return AppException.RequestCreateItem( {"ERROR": f"Error creating championship: {str(e)}"})

    async def get(self, model, id: int) -> ChampionshipModel:
        """
        Retrieve record by id.
        """
        try:
            result = self.db.query(model).filter(model.id == id).first()
            return result
        except Exception as e:
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving championship: {str(e)}"})

    async def update(self, model, id: int, schema) -> ChampionshipModel:
        """
        Update record by id.
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

    async def delete(self, model, id: int) -> ChampionshipModel:
        """
        Delete record by id.
        """
        try:
            record = self.db.query(model).filter(model.id == id).first()
            if not record:
                raise ValueError("Record not found")
            self.db.delete(record)
            self.db.commit()
            return record
        except Exception as e:
            return AppException.RequestUpdateItem( {"ERROR": f"Error deleting championship: {str(e)}"})