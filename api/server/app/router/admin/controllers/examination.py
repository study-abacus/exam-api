from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session


from app.utils.service_request import handle_result
from app.schemas.examination import ExaminationBase, ExaminationCreate, Examination, ExaminationUpdate
from app.services.examination import ExaminationService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()



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
