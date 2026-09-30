from datetime import datetime, timedelta
from jose import jwt # type: ignore
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from  fastapi import Depends
from dotenv import load_dotenv
import os
from jose import JWTError
from fastapi import HTTPException

load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    token = credentials.credentials
    payload = verify_token(token)
    return payload["sub"]