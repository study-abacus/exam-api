from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session


from app.utils.service_request import handle_result
from app.schemas.examination import ExaminationAttempts, ExaminationCreate, Examination, ExaminationUpdate
from app.services.examination import ExaminationService
from app.services.exam_attempt import ExamAttemptCRUD

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Examination])
async def read_examinations_for_championship(championship_id:int , skip: int = 0, limit: int = 100,  db: Session = Depends(deps.get_session)):
    """
    Retrieve examinations for championship.
    """
    result = await ExaminationService(db).get_championship_examinations(championship_id, skip=skip, limit=limit)
    return handle_result(result)


@router.get("/{examination_id}/", response_model=ExaminationAttempts)
async def read_examination(examination_id: int, db: Session = Depends(deps.get_session), cache = Depends(deps.get_cache), payload : dict = Depends(deps.valid_attempt)):
    """
    Retrieve examination.
    """
    result = await ExaminationService(db, cache).get_examination(examination_id, payload['admit_card_id'] )
    return handle_result(result)

@router.post("/{examination_id}/submit", status_code=status.HTTP_201_CREATED)
async def submit_exam(examination_id:int, db: Session = Depends(deps.get_session), cache = Depends(deps.get_cache), payload : dict = Depends(deps.valid_attempt)):
    """
    Submit an exam
    """
    await ExamAttemptCRUD(db, cache).update(examination_id, payload['admit_card_id'] )
     


