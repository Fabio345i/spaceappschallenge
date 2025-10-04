from fastapi import APIRouter, HTTPException
from db import session
from routes.auth import schemas, utils

router = APIRouter()

@router.post("/register")
async def register(user: schemas.UserCreate):
    existing = await session.db["users"].find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = utils.hash_password(user.password)
    user_doc = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_pw,
    }

    result = await session.db["users"].insert_one(user_doc)
    return {"message": "User created", "user_id": str(result.inserted_id)}