from fastapi import APIRouter, Depends
from api.routes.auth.dependencies import get_current_user
from api.db import session
from bson import ObjectId

router = APIRouter(tags=["Favorites"])

@router.post("/favorites")
async def add_favorite(favorite: dict, current_user: dict = Depends(get_current_user)):
    """
    favorite attendu: { name: str, lat: float, lon: float }
    """
    favorites = current_user.get("favorites", [])
    if any(f["name"] == favorite["name"] for f in favorites):
        return {"status": "exists"}

    await session.db["users"].update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$push": {"favorites": favorite}}
    )
    return {"status": "ok", "favorite": favorite}

@router.get("/favorites")
async def get_favorites(current_user: dict = Depends(get_current_user)):
    return current_user.get("favorites", [])
