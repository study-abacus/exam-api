from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from app.utils.service_request import handle_result
from app.schemas.question import QuestionBase, QuestionCreate, Question, QuestionUpdate
from app.services.question import QuestionService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
