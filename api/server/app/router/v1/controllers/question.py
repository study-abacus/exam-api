from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from app.utils.service_request import handle_result
from app.schemas.question import QuestionBase, QuestionAuth, Question, QuestionUpdate
from app.services.question import QuestionService
from app.services.examination import ExaminationCRUD
from app.services.exam_attempt import ExamAttemptCRUD


from app.router import deps
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[QuestionAuth])
async def read_questions( cache = Depends(deps.get_cache), db: Session = Depends(deps.get_session),  payload : dict = Depends(deps.valid_attempt)):
    """
    Retrieve questions.
    """
    err = await deps.valid_exam(payload["examination_id"], payload['admit_card_id'], db, cache)
    if err:
        return handle_result(err)
    questions = await QuestionService(db, cache).get_examination_questions(payload["examination_id"], payload['admit_card_id'])
    return handle_result(questions)

@router.get("/{question_id}", response_model=QuestionAuth)
async def read_question(question_id: int, cache = Depends(deps.get_cache), db: Session = Depends(deps.get_session),  payload : dict = Depends(deps.valid_attempt)):
    """
    Retrieve question.
    """
    err = await deps.valid_exam(payload["examination_id"], payload['admit_card_id'], db, cache)
    if err:
        return handle_result(err)
    result = await QuestionService(db, cache).get_question(question_id,  payload['admit_card_id'])
    # print(f' res {handle_result(result)}')
    return handle_result(result)


@router.put("/{question_id}", response_model=QuestionAuth)
async def answer_question(question_id: int, question: QuestionUpdate, cache = Depends(deps.get_cache), db: Session = Depends(deps.get_session),  payload : dict = Depends(deps.valid_attempt)):
    """
    Answer question.
    """
    # get exam details from cache and verify if the question_id is in the exam
    
    err = await deps.valid_exam(payload["examination_id"], payload['admit_card_id'], db, cache)
    if err:
        return handle_result(err)
    result = await QuestionService(db, cache).answer_question(question_id, payload['admit_card_id'], question.answer)
    return handle_result(result)
