from fastapi import Query, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional, Generator


from app.db.session import SessionDB
from app.db.redis import Redis
from app.utils.jwt import decode_jwt_token


import json
import logging


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_session() -> Generator:
    db = SessionDB()
    db_session = db.get_session()
    if db_session is None:
        raise ValueError("DB Session is not set. Please check the configuration.")
    try:
        yield db_session
        db_session.commit()  
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
