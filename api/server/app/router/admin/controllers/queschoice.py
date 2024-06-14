from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from utils.service_request import handle_result
from schemas.queschoice import QuesChoiceBase, QuesChoiceCreate, QuesChoice, QuesChoiceUpdate
from services.queschoice import QuesChoiceService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[QuesChoice])
async def read_queschoices(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve queschoices.
    """
    result = await QuesChoiceService(db).get_queschoices( skip=skip, limit=limit)
    return handle_result(result)

@router.post("/{question_id}", response_model=QuesChoice)
async def create_queschoice(question_id: int, queschoice: QuesChoiceCreate, db: Session = Depends(deps.get_session)):
    """
    Create new queschoice.
    """
    result = await QuesChoiceService(db).create_queschoice(question_id, queschoice)
    return handle_result(result)

@router.get("/{queschoice_id}", response_model=QuesChoice)
async def read_queschoice(queschoice_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve queschoice.
    """
    result = await QuesChoiceService(db).get_queschoice(queschoice_id)
    return handle_result(result)

@router.put("/{queschoice_id}", response_model=QuesChoice)
async def update_queschoice(queschoice_id: int, queschoice: QuesChoiceUpdate, db: Session = Depends(deps.get_session)):
    """
    Update queschoice.
    """
    result = await QuesChoiceService(db).update_queschoice(queschoice_id, queschoice)
    return handle_result(result)

@router.delete("/{queschoice_id}")
async def delete_queschoice(queschoice_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete queschoice.
    """
    result = await QuesChoiceService(db).delete_queschoice(queschoice_id)
    return handle_result(result)

@router.get("/{question_id}/queschoices", response_model=List[QuesChoice])
async def read_question_queschoices(question_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve queschoices for question.
    """
    result = await QuesChoiceService(db).get_queschoices_by_question(question_id)
    return handle_result(result)