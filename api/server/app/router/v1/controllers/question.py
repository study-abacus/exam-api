from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from app.utils.service_request import handle_result
from app.schemas.question import QuestionBase, QuestionAuth, Question, QuestionUpdate
from app.services.question import QuestionService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Question])
def read_questions(exam_id: Optional[int] = None, cache = Depends(deps.get_cache), db: Session = Depends(deps.get_session)):
    """
    Retrieve questions.
    """
    #get from the questions from cache using exam_id (exam_id_{exam_id})
    if exam_id:
        questions = cache.get(f"exam_{exam_id}")
        if questions:
            return questions
    result = QuestionService(db).get_examination_questions(exam_id)
    return handle_result(result)

@router.get("/", response_model=QuestionAuth)
def read_question(question_id: int, cache = Depends(deps.get_cache), db: Session = Depends(deps.get_session)):
    """
    Retrieve question.
    """
    #get from the questions from cache using question_id (question_id_{question_id})
    question = cache.get(f"question_{question_id}")
    if question:
        return question
    result = QuestionService(db).get_question(question_id)
    return handle_result(result)

"""
## [PUT] questions?{question_id}?{exam_id} --> [AUTHENTICATE]
    1. cache (exam_id)
    2. verify question_id in exam_id
    3. upsert the question_attempt

    Response :  {
        question : str
        question options: str
        user_answer: str
    }



"""

@router.put("/", response_model=QuestionAuth)
def update_question(question_id: int, exam_id: int, question: QuestionUpdate, cache = Depends(deps.get_cache), db: Session = Depends(deps.get_session)):
    """
    Update question.
    """
    # get exam details from cache and verify if the question_id is in the exam
    exam = cache.get(f"exam_{exam_id}")
    if not exam:
        return handle_result({"ERROR": "Exam not found"})
    if question_id not in exam["questions"]:
        return handle_result({"ERROR": "Question not found in exam"})
    result = QuestionService(db).update_question(question_id, exam_id,exam, question)
    return handle_result(result)
