from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from app.utils.service_request import handle_result
from app.schemas.admit_card import AdmitCardBase, AdmitCardCreate, AdmitCard, AdmitCardUpdate
from app.services.admit_card import AdmitCardService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[AdmitCard])
async def read_admit_cards(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards.
    """
    result = await AdmitCardService(db).get_admit_cards( skip=skip, limit=limit)
    return handle_result(result)


"""
Input: AdmitCard_id ; password 
"""
@router.post("/auth", response_model=List[AdmitCard])
async def read_admit_cards(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards.
    """
    result = await AdmitCardService(db).get_admit_cards( skip=skip, limit=limit)
    return handle_result(result)



@router.post("/{profile_id}", response_model=AdmitCard)
async def create_admit_card(profile_id: int, admit_card: AdmitCardCreate, championship_id: int= Depends(deps.championship_id_param), examination_ids : List[int] = Depends(deps.examination_ids_param), db: Session = Depends(deps.get_session)):
    """
    Create new admit_card.
    """
    result = await AdmitCardService(db).create_admit_card(profile_id, championship_id, examination_ids, admit_card)
    return handle_result(result)

# @router.get("/{admit_card_id}", response_model=AdmitCard)
# async def read_admit_card(admit_card_id: int, db: Session = Depends(deps.get_session)):
#     """
#     Retrieve admit_card.
#     """
#     result = await AdmitCardService(db).get_admit_card(admit_card_id)
#     return handle_result(result)

@router.put("/{admit_card_id}", response_model=AdmitCard)
async def update_admit_card(admit_card_id: int, admit_card: AdmitCardUpdate,championship_id: int= Depends(deps.championship_id_param), examination_ids : List[int] = Depends(deps.examination_ids_param), db: Session = Depends(deps.get_session)):
    """
    Update admit_card.
    """
    result = await AdmitCardService(db).update_admit_card(admit_card_id, admit_card, championship_id, examination_ids)
    return handle_result(result)

@router.delete("/{admit_card_id}")
async def delete_admit_card(admit_card_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete admit_card.
    """
    result = await AdmitCardService(db).delete_admit_card(admit_card_id)
    return handle_result(result)


@router.get("/profiles/{profile_id}/admit_cards", response_model=List[AdmitCard])
async def read_profile_admit_cards(profile_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards for profile.
    """
    result = await AdmitCardService(db).get_profile_admit_cards(profile_id)
    return handle_result(result)

@router.get("/championships/{championship_id}/admit_cards", response_model=List[AdmitCard])
async def read_championship_admit_cards(championship_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards for championship.
    """
    result = await AdmitCardService(db).get_championship_admit_cards(championship_id)
    return handle_result(result)

@router.get("/examinations/{examination_id}/admit_cards", response_model=List[AdmitCard])
async def read_examination_admit_cards(examination_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards for examination.
    """
    result = await AdmitCardService(db).get_examination_admit_cards(examination_id)
    return handle_result(result)

@router.get("/{profile_id}/championship/{championship_id}/admit_cards", response_model=List[AdmitCard])
async def read_profile_championship_admit_cards(profile_id: int, championship_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards for profile and championship.
    """
    result = await AdmitCardService(db).get_profile_championship_admit_cards(profile_id, championship_id)
    return handle_result(result)

@router.get("/{profile_id}/examination/{examination_id}/admit_cards", response_model=List[AdmitCard])
async def read_profile_examination_admit_cards(profile_id: int, examination_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve admit_cards for profile and examination.
    """
    result = await AdmitCardService(db).get_profile_examination_admit_cards(profile_id, examination_id)
    return handle_result(result)

