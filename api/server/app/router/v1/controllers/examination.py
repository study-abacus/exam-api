from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session


from utils.service_request import handle_result
from schemas.examination import ExaminationBase, ExaminationCreate, Examination, ExaminationUpdate
from services.examination import ExaminationService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Examination])
async def read_examinations(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve examinaapi/server/app/services/examination.pytions.
    """
    result = await ExaminationService(db).get_examinations( skip=skip, limit=limit)
    return handle_result(result)

@router.post("/{championship_id}", response_model=Examination)
async def create_examination(championship_id: int, examination: ExaminationCreate, db: Session = Depends(deps.get_session)):
    """
    Create new examination.
    """
    result = await ExaminationService(db).create_examination(championship_id, examination)
    return handle_result(result)

@router.get("/{examination_id}", response_model=Examination)
async def read_examination(examination_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve examination.
    """
    result = await ExaminationService(db).get_examination(examination_id)
    return handle_result(result)

@router.put("/{examination_id}", response_model=Examination)
async def update_examination(examination_id: int, examination: ExaminationUpdate, db: Session = Depends(deps.get_session)):
    """
    Update examination.
    """
    result = await ExaminationService(db).update_examination(examination_id, examination)
    return handle_result(result)

@router.delete("/{examination_id}")
async def delete_examination(examination_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete examination.
    """
    result = await ExaminationService(db).delete_examination(examination_id)
    return handle_result(result)

@router.get("/{championship_id}/examinations", response_model=List[Examination])
async def read_championship_examinations(championship_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve examinations for championship.
    """
    result = await ExaminationService(db).get_championship_examinations(championship_id)
    return handle_result(result)