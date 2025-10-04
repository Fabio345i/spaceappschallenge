from fastapi import APIRouter, HTTPException
from db import session
from routes.auth import schemas, utils
from datetime import timedelta, timezone

router = APIRouter()

@router.post("/login")
async def login(user: schemas.UserLogin):
    db_user = await session.db["users"].find_one({"username": user.username})
    if not db_user or not utils.verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = utils.create_access_token(
        {"id": str(db_user["_id"])},
        expires_delta=timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}