from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session


from app.utils.service_request import handle_result
from app.schemas.championship import ChampionshipBase, ChampionshipCreate, Championship, ChampionshipUpdate
from app.services.championship import ChampionshipService


from app.router import deps
import logging


logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/", response_model=List[Championship])
async def read_championships(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve championships.
    """
    result = await ChampionshipService(db).get_championships( skip=skip, limit=limit)
    return handle_result(result)


@router.get("/{championship_id}/", response_model=Championship)
async def read_championship(championship_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve championship.
    """
    result = await ChampionshipService(db).get_championship(championship_id)
    return handle_result(result)
