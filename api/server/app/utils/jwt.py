

#create jwt token of admit card object
from typing import Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas.admit_card import AdmitCard
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_jwt_token(admit_card: AdmitCard) -> Any:
    """
    Create jwt token of admit card object.
    """

    to_encode = admit_card.__dict__
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str) -> Any:
    """
    Decode jwt token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None