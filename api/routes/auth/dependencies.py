from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from api.db import session
from .utils import SECRET_KEY, ALGORITHM
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_error
    except JWTError:
        raise credentials_error
    
    if not ObjectId.is_valid(user_id):
        raise credentials_error

    user = await session.db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise credentials_error
    return user
