from datetime import datetime
from jose import jwt, JWTError
from app.config import settings

def veryfy_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    
    except JWTError:
        raise ValueError("Invalid or expired token")