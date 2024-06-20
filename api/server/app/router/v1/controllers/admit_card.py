from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from app.utils.service_request import handle_result
from app.utils.jwt import decode_jwt_token
from app.schemas.admit_card import AdmitCardAuthenticateBase,AdmitCardAuthenticate, AdmitCardCreate, AdmitCard, AdmitCardUpdate, AdmitCardCreateManual
from app.schemas.profile import ProfileUpdate, Profile
from app.services.admit_card import AdmitCardService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/authenticate/")
async def authenticate_admit_card(admit_card: AdmitCardAuthenticateBase, db: Session = Depends(deps.get_session)):
    """
    Authenticate admit_card.
    """
    result = await AdmitCardService(db).authenticate_admit_card(admit_card)
    return handle_result(result)


@router.put("/current/", response_model=Profile)
async def create_current_admit_card(profile:ProfileUpdate,admit_card:dict = Depends(deps.get_admit_card), db: Session = Depends(deps.get_session)):
    """
    Create new admit_card.
    """
    result = await AdmitCardService(db).update_current_admit_card(profile,admit_card)
    return handle_result(result)

@router.get("/current/", response_model=Profile)
async def create_current_admit_card(admit_card:dict = Depends(deps.get_admit_card), db: Session = Depends(deps.get_session)):
    """
    Create new admit_card.
    """
    result = await AdmitCardService(db).get_current_admit_card(admit_card)
    return handle_result(result)
