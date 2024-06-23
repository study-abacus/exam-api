from app.utils.app_exceptions import AppException

from app.services.main import AppService, AppCRUD
from app.utils.service_request import ServiceResult

from app.models.profile import Profile as ProfileModel
from app.schemas.profile import Profile as ProfileSchema

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

import logging
import requests
import datetime

logger = logging.getLogger(__name__)

class ProfileService(AppService):

    async def get_profiles(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve profiles.
        """
        try:
            result = await ProfileCRUD(self.db).get_all(ProfileModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving profiles: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving profiles: {str(e)}"}))

    async def create_profile(self, profile: ProfileSchema) -> ServiceResult:
        """
        Create new profile.
        """
        try:
            result = await ProfileCRUD(self.db).create(ProfileModel, profile)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating profile: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating profile: {str(e)}"}))
    
    async def get_profile(self, profile_id: int) -> ServiceResult:
        """
        Retrieve profile.
        """
        try:
            result = await ProfileCRUD(self.db).get(ProfileModel, profile_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving profile: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving profile: {str(e)}"}))

    async def update_profile(self, profile_id: int, profile: ProfileSchema) -> ServiceResult:
        """
        Update profile.
        """
        try:
            result = await ProfileCRUD(self.db).update(ProfileModel, profile_id, profile)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error updating profile: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating profile: {str(e)}"}))

    async def delete_profile(self, profile_id: int) -> ServiceResult:
        """
        Delete profile.
        """
        try:
            result = await ProfileCRUD(self.db).delete(ProfileModel, profile_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error deleting profile: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting profile: {str(e)}"}))

class ProfileCRUD(AppCRUD):

    async def get_all(self, model: ProfileModel, skip: int = 0, limit: int = 100, filters : Optional[List[Any]] = None) -> List[ProfileModel]:
        """
        Retrieve all profiles.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(and_(*filters))
            result = query.order_by(asc(model.id)).offset(skip).limit(limit).all()
            return result
        except Exception as e:
            logger.error(f'Error retrieving profiles: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving profiles: {str(e)}"})
        
    async def create_inital_profile(self, order):
        """
        Create initial profile.
        """
        try:
            new_profile = ProfileModel(
                name = order['name'],
                ci = "",
                email = order['email'],
                phone = order['phone'],
                sa_class = "",
                age = "",
                city = "",
                country = "",
                guardian_name = ""
            )
            self.db.add(new_profile)
            self.db.commit()
            self.db.refresh(new_profile)

            return new_profile
        except Exception as e:
            logger.error(f'Error creating initial profile: {str(e)}')
            return AppException.RequestCreateItem( {"ERROR": f"Error creating initial profile: {str(e)}"})


    async def create(self, model: ProfileModel, profile: ProfileSchema) -> ProfileModel:
        """
        Create new profile.
        """
        try:
            new_profile = model(**profile.dict())
            self.db.add(new_profile)
            self.db.commit()
            self.db.refresh(new_profile)
            return new_profile
        except Exception as e:
            logger.error(f'Error creating profile: {str(e)}')
            return AppException.RequestCreateItem( {"ERROR": f"Error creating profile: {str(e)}"})

    async def get(self,  profile_id: int,model= ProfileModel) -> ProfileModel:
        """
        Retrieve profile.
        """
        try:
            result = self.db.query(model).filter(model.id == profile_id).first()
            return result
        except Exception as e:
            logger.error(f'Error retrieving profile: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving profile: {str(e)}"})

    async def update(self, id: int, schema ,model= ProfileModel) -> ProfileModel:
        """
        Update profile.
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
            logger.error(f'Error updating profile: {str(e)}')
            return AppException.RequestUpdateItem( {"ERROR": f"Error updating profile: {str(e)}"})

    async def delete(self, model: ProfileModel, profile_id: int) -> ProfileModel:
        """
        Delete profile.
        """
        try:
            result = self.db.query(model).filter(model.id == profile_id).delete()
            self.db.commit()
            return result
        except Exception as e:
            logger.error(f'Error deleting profile: {str(e)}')
            return AppException.RequestDeleteItem( {"ERROR": f"Error deleting profile: {str(e)}"})



    
