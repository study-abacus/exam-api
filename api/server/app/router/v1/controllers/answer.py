from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from utils.service_request import handle_result
from schemas.answer import AnswerBase, AnswerCreate, Answer, AnswerUpdate
from services.answer import AnswerService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Answer])
async def read_answers(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve answers.
    """
    result = await AnswerService(db).get_answers( skip=skip, limit=limit)
    return handle_result(result)

@router.post("/{question_id}", response_model=Answer)
async def create_answer(question_id: int, answer: AnswerCreate, db: Session = Depends(deps.get_session)):
    """
    Create new answer.
    """
    result = await AnswerService(db).create_answer(question_id, answer)
    return handle_result(result)

@router.get("/{answer_id}", response_model=Answer)
async def read_answer(answer_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve answer.
    """
    result = await AnswerService(db).get_answer(answer_id)
    return handle_result(result)

@router.put("/{answer_id}", response_model=Answer)
async def update_answer(answer_id: int, answer: AnswerUpdate, db: Session = Depends(deps.get_session)):
    """
    Update answer.
    """
    result = await AnswerService(db).update_answer(answer_id, answer)
    return handle_result(result)

@router.delete("/{answer_id}")
async def delete_answer(answer_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete answer.
    """
    result = await AnswerService(db).delete_answer(answer_id)
    return handle_result(result)

@router.get("/{question_id}/answers", response_model=List[Answer])
async def read_question_answers(question_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve answers for question.
    """
    result = await AnswerService(db).get_question_answers(question_id)
    return handle_result(result)