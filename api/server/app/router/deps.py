from fastapi import Query
from typing import Optional, Generator


from db.session import SessionDB


import json
import logging


def get_session() -> Generator:
    db = SessionDB()
    db_session = db.get_session()
    if db_session is None:
        raise ValueError("DB Session is not set. Please check the configuration.")
    try:
        yield db_session
    finally:
        db_session.close()




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


