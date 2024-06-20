from utils.app_exceptions import AppException

from services.main import AppService, AppCRUD
from utils.service_request import ServiceResult
from utils.hash import hash_password
from utils.jwt import create_jwt_token

from models.admit_card import AdmitCard as AdmitCardModel
from schemas.admit_card import(
    AdmitCardCreate as AdmitCardCreateSchema,
    AdmitCard as AdmitCardSchema,
    AdmitCardAuthenticateBase
)
from schemas.profile import ProfileUpdate
from services.profile import ProfileCRUD

from sqlalchemy import asc, desc, and_
from typing import List, Any , Optional, Union

import logging
import requests
import datetime

logger = logging.getLogger(__name__)

class AdmitCardService(AppService):

    async def get_current_admit_card(self,admit_card:dict) -> ServiceResult:
        """
        Retrieve current admit_card.
        """
        try:
            result = await ProfileCRUD(self.db).get( admit_card['profile_id'])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_card: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_card: {str(e)}"}))

    async def update_current_admit_card(self,profile:ProfileUpdate, admit_card: dict) -> ServiceResult:
        """
        Update current admit_card.
        """
        try:
            profile = await ProfileCRUD(self.db).update(admit_card['profile_id'], profile)
            return ServiceResult(profile)
        except Exception as e:
            logger.error(f'Error updating admit_card: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating admit_card: {str(e)}"}))
    
    async def authenticate_admit_card(self, admit_card: AdmitCardAuthenticateBase) -> ServiceResult:
        """
        Authenticate admit_card.
        """
        try:
            _admit_card = await AdmitCardCRUD(self.db).get(AdmitCardModel, admit_card.id)
            hashed_password = await hash_password(admit_card.password)
            if _admit_card.password_hash == hashed_password:
                _admit_card.password_hash = None
                _admit_card._sa_instance_state = None
                token = create_jwt_token(_admit_card)
                return ServiceResult({"jwt": token})
            else:
                return ServiceResult(AppException.RequestAuthenticateItem( {"ERROR": "Invalid password"}))
        except Exception as e:
            logger.error(f'Error authenticating admit_card: {str(e)}')
            return ServiceResult(AppException.RequestAuthenticateItem( {"ERROR": f"Error authenticating admit_card: {str(e)}"}))

    async def get_admit_cards(self, skip: int = 0, limit: int = 100) -> ServiceResult:
        """
        Retrieve admit_cards.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, skip=skip, limit=limit)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

    async def create_admit_card(self, profile_id: int, championship_id: int, examination_ids: List[int], admit_card: AdmitCardCreateSchema) -> ServiceResult:
        """
        Create new admit_card.
        """
        try:
            result = await AdmitCardCRUD(self.db).create( profile_id, championship_id, examination_ids, admit_card)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error creating admit_card: {str(e)}')
            return ServiceResult(AppException.RequestCreateItem( {"ERROR": f"Error creating admit_card: {str(e)}"}))

    async def get_admit_card(self, admit_card_id: int) -> ServiceResult:
        """
        Retrieve admit_card.
        """
        try:
            result = await AdmitCardCRUD(self.db).get(AdmitCardModel, admit_card_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_card: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_card: {str(e)}"}))
    
    async def update_admit_card(self, admit_card_id: int, admit_card: AdmitCardSchema, championship_id: int, examination_ids: List[int]) -> ServiceResult:
        """
        Update admit_card.
        """
        try:
            result = await AdmitCardCRUD(self.db).update(AdmitCardModel, admit_card_id, admit_card, championship_id, examination_ids)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error updating admit_card: {str(e)}')
            return ServiceResult(AppException.RequestUpdateItem( {"ERROR": f"Error updating admit_card: {str(e)}"}))

    async def delete_admit_card(self, admit_card_id: int) -> ServiceResult:
        """
        Delete admit_card.
        """
        try:
            result = await AdmitCardCRUD(self.db).delete(AdmitCardModel, admit_card_id)
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error deleting admit_card: {str(e)}')
            return ServiceResult(AppException.RequestDeleteItem( {"ERROR": f"Error deleting admit_card: {str(e)}"}))

    async def get_profile_admit_cards(self, profile_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on profile.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.profile_id == profile_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

    async def get_championship_admit_cards(self, championship_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on championship.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.championship_id == championship_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

    async def get_examination_admit_cards(self, examination_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on examination.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.examination_ids.contains([examination_id])])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

    async def get_profile_championship_admit_cards(self, profile_id: int, championship_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on profile and championship.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.profile_id == profile_id, AdmitCardModel.championship_id == championship_id])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))
    
    async def get_profile_examination_admit_cards(self, profile_id: int, examination_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on profile and examination.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.profile_id == profile_id, AdmitCardModel.examination_ids.contains([examination_id])])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

    async def get_championship_examination_admit_cards(self, championship_id: int, examination_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on championship and examination.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.championship_id == championship_id, AdmitCardModel.examination_ids.contains([examination_id])])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

    async def get_profile_championship_examination_admit_cards(self, profile_id: int, championship_id: int, examination_id: int) -> ServiceResult:
        """
        Retrieve admit_cards based on profile, championship and examination.
        """
        try:
            result = await AdmitCardCRUD(self.db).get_all(AdmitCardModel, filters=[AdmitCardModel.profile_id == profile_id, AdmitCardModel.championship_id == championship_id, AdmitCardModel.examination_ids.contains([examination_id])])
            return ServiceResult(result)
        except Exception as e:
            logger.error(f'Error retrieving admit_cards: {str(e)}')
            return ServiceResult(AppException.RequestGetItem( {"ERROR": f"Error retrieving admit_cards: {str(e)}"}))

class AdmitCardCRUD(AppCRUD):

    async def get_all(self, model, skip: int = 0, limit: int = 100 , filters: Optional[List[Any]] = None) -> ServiceResult:
        """
        Retrieve all items.
        """
        try:
            query = self.db.query(model)
            if filters:
                query = query.filter(*filters)
            return query.order_by(asc(model.id)).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f'Error retrieving items: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving items: {str(e)}"})

    async def create(self, profile_id: int, championship_id: int, examination_ids: List[int], item: dict) -> ServiceResult:
        """
        Create new item.
        """
        try:
            item = AdmitCardModel(**item.dict(), profile_id=profile_id, championship_id=championship_id, examination_ids=examination_ids)
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except Exception as e:
            logger.error(f'Error creating item: {str(e)}')
            return AppException.RequestCreateItem( {"ERROR": f"Error creating item: {str(e)}"})

    async def get(self, model, item_id: int) -> ServiceResult:
        """
        Retrieve item by id.
        """
        try:
            item = self.db.query(model).filter(model.id == item_id).first()
            return item
        except Exception as e:
            logger.error(f'Error retrieving item: {str(e)}')
            return AppException.RequestGetItem( {"ERROR": f"Error retrieving item: {str(e)}"})

    async def update(self, model, item_id: int, item: dict, championship_id: int, examination_ids: List[int]) -> ServiceResult:
        """
        Update item by id.
        """
        try:
            record = self.db.query(model).filter(model.id == item_id).first()
            record.order_id = item.order_id
            record.championship_id = championship_id
            record.examination_ids = examination_ids
            self.db.commit()
            self.db.refresh(record)
            return record
        except Exception as e:
            logger.error(f'Error updating item: {str(e)}')
            return AppException.RequestUpdateItem( {"ERROR": f"Error updating item: {str(e)}"})

    async def delete(self, model, item_id: int) -> ServiceResult:
        """
        Delete item by id.
        """
        try:
            item = self.db.query(model).filter(model.id == item_id).first()
            self.db.delete(item)
            self.db.commit()
            return item
        except Exception as e:
            logger.error(f'Error deleting item: {str(e)}')
            return AppException.RequestDeleteItem( {"ERROR": f"Error deleting item: {str(e)}"})
    
