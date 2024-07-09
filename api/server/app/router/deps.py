from fastapi import Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.utils.app_exceptions import AppException
from typing import Optional, Generator


from app.db.session import SessionDB
from app.db.redis import Redis
from app.utils.service_request import ServiceResult
from app.services.examination import ExaminationCRUD
from app.services.exam_attempt import ExamAttemptCRUD
from app.utils.jwt import decode_jwt_token


import json
import logging
import pytz
from datetime import datetime
from jose.exceptions import ExpiredSignatureError, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


logger = logging.getLogger(__name__)


def get_session() -> Generator:
    db = SessionDB()
    db_session = db.get_session()
    if db_session is None:
        raise ValueError("DB Session is not set. Please check the configuration.")
    try:
        yield db_session
        # db_session.commit()  
    except:
        db_session.rollback()  
        raise
    finally:
        db_session.close()  



def get_cache() -> Generator:
    cache = Redis()
    cache_client = cache.client
    if cache_client is None:
        raise ValueError("Cache client is not set. Please check the configuration.")
    try:
        yield cache_client
    finally:
        cache_client.close()



def get_filters(query_params: dict):
    return {key: Query(None, **value) for key, value in query_params.items()}


def query_param(filters: Optional[str] = Query(None, description="Filter parameters as a JSON string")):
    if filters is not None:
        try:
            filters = json.loads(filters)
        except json.JSONDecodeError as e:
            logging.error(e.__cause__)
            return {"error": "Invalid query parameter format"}


    return filters


def body_param(body: Optional[str] = Query(None, description="Body parameters as a JSON string")):
    if body is not None:
        try:
            body = json.loads(body)
        except json.JSONDecodeError as e:
            logging.error(e.__cause__)
            return {"error": "Invalid body parameter format"}


    return body


#given comman separated list convert to list
def examination_ids_param(examination_ids: Optional[str] = Query(None, description="Comma separated list of examination ids")):
    try:
        if examination_ids is not None:
            examination_ids = examination_ids.split(",") if "," in examination_ids else [examination_ids]
        return examination_ids
    except Exception as e:
        return None

def championship_id_param(championship_id: Optional[int] = Query(None, description="Championship id")):
    try:
        return championship_id
    except Exception as e:
        return None
    
def get_order(championship_id: int , examination_ids: str = Query(None, description="Comma separated list of examination ids")):
    try:
        order = {
            "championship_id": championship_id,
            "examination_ids": examination_ids.split(",") if "," in examination_ids else [examination_ids]
        }
        return order
    except Exception as e:
        return None
    
def get_admit_card(token: str = Depends(oauth2_scheme)):
    try:
        return decode_jwt_token(token)
    except Exception as e:
        return None

async def valid_attempt(examination_id: int,token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_jwt_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"JWT token invalid: {e}")
    
    try:

        exam_ids = payload["examination_ids"]
        current_time = datetime.utcnow()
        expiration_time = payload.get("exp")
        if expiration_time and expiration_time < current_time.timestamp():
            raise ValueError("Token has expired")


        if not exam_ids:
            raise HTTPException(status_code=401, detail="Invalid JWT payload: exam_id missing")

        if examination_id not in exam_ids:
            raise HTTPException(status_code=403, detail="Exam ID mismatch")

        return {
            "admit_card_id" : payload['id'],
            "examination_id" :examination_id,
            "admit_card" : payload
        }

    except ExpiredSignatureError:
        logger.error("JWT expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        logger.error(f"Error decoding JWT: {str(e)}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    except (ValueError, TypeError) as e:
        logger.error(f"Error parsing user ID from JWT: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=401, detail="Unauthorized")

async def valid_exam(examination_id: int, admit_card_id: int, db, cache):
    if admit_card_id == 1000:
        exam_attempt = await ExamAttemptCRUD(db, cache).get_create(examination_id, admit_card_id)
        if exam_attempt.is_submitted:
            return ServiceResult(AppException.ExamSubmitted({'ERROR': 'Examination has already been submitted!'}))
        return
    
    exam_details = await ExaminationCRUD(db, cache).get(examination_id)
    
    if datetime.now(pytz.utc) < exam_details.exam_start_dt:
        return ServiceResult(AppException.ExaminationNotStarted({'ERROR': 'Examination has not started yet!'}))
    
    exam_attempt = await ExamAttemptCRUD(db, cache).get_create(examination_id, admit_card_id)
    
    if exam_attempt.is_submitted:
        return ServiceResult(AppException.ExamSubmitted({'ERROR': 'Examination has already been submitted!'}))
        