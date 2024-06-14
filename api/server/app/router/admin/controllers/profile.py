from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any , Optional, Union
from sqlalchemy.orm import Session

from utils.service_request import handle_result
from schemas.profile import ProfileBase, ProfileCreate, Profile, ProfileUpdate
from services.profile import ProfileService

from app.router import deps
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[Profile])
async def read_profiles(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_session)):
    """
    Retrieve profiles.
    """
    result = await ProfileService(db).get_profiles( skip=skip, limit=limit)
    return handle_result(result)

@router.post("/", response_model=Profile)
async def create_profile(profile: ProfileCreate, db: Session = Depends(deps.get_session)):
    """
    Create new profile.
    """
    result = await ProfileService(db).create_profile(profile)
    return handle_result(result)

@router.get("/{profile_id}", response_model=Profile)
async def read_profile(profile_id: int, db: Session = Depends(deps.get_session)):
    """
    Retrieve profile.
    """
    result = await ProfileService(db).get_profile(profile_id)
    return handle_result(result)

@router.put("/{profile_id}", response_model=Profile)
async def update_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(deps.get_session)):
    """
    Update profile.
    """
    result = await ProfileService(db).update_profile(profile_id, profile)
    return handle_result(result)

@router.delete("/{profile_id}")
async def delete_profile(profile_id: int, db: Session = Depends(deps.get_session)):
    """
    Delete profile.
    """
    result = await ProfileService(db).delete_profile(profile_id)
    return handle_result(result)