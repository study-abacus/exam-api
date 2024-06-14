from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session


from utils.service_request import handle_result
from schemas.championship import ChampionshipBase, ChampionshipCreate, Championship, ChampionshipUpdate
from services.championship import ChampionshipService


from app.router import deps
import logging


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/", response_model=Championship)
async def create_championship(championship: ChampionshipCreate, db: Session = Depends(deps.get_session)):
    """
    Create new championship.
    """
    result = await ChampionshipService(db).create_championship(championship)
    return handle_result(result)



@router.put("/{championship_id}", response_model=Championship)
async def update_championship(championship_id: int, championship: ChampionshipUpdate, db: Session = Depends(deps.get_session)):
    """
    Update championship.
    """
    result = await ChampionshipService(db).update_championship(championship_id, championship)
    return handle_result(result)

@router.delete("/{championship_id}",include_in_schema = False)
async def delete_championship(championship_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete championship.
    """
    result = await ChampionshipService(db).delete_championship(championship_id)
    return handle_result(result)

