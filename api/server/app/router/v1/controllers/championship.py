from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session


from utils.service_request import handle_result
from schemas.championship import *
from services.championship import *


from app.router import deps
import logging


logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/")
async def read_users(db: Session = Depends(deps.get_session)):
    return "Hello WOrld"