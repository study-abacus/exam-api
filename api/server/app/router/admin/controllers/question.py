from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from utils.service_request import handle_result
from schemas.question import QuestionBase, QuestionCreate, Question, QuestionUpdate
from services.question import QuestionService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{examination_id}", response_model=Question)
async def create_question(examination_id: int, question: QuestionCreate, db: Session = Depends(deps.get_session)):
    """
    Create new question.
    """
    result = await QuestionService(db).create_question(examination_id, question)
    return handle_result(result)

@router.get("/{question_id}", response_model=Question)
async def read_question(question_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve question.
    """
    result = await QuestionService(db).get_question(question_id)
    return handle_result(result)

@router.put("/{question_id}", response_model=Question)
async def update_question(question_id: int, question: QuestionUpdate, db: Session = Depends(deps.get_session)):
    """
    Update question.
    """
    result = await QuestionService(db).update_question(question_id, question)
    return handle_result(result)

@router.delete("/{question_id}")
async def delete_question(question_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete question.
    """
    result = await QuestionService(db).delete_question(question_id)
    return handle_result(result)


@router.get("/{examination_id}/questions", response_model=List[Question])
async def read_examination_questions(examination_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve questions for examination.
    """
    result = await QuestionService(db).get_examination_questions(examination_id)
    return handle_result(result)
