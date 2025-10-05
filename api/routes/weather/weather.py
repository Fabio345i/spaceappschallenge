from fastapi import APIRouter, HTTPException, Query
import requests
import pandas as pd
import io
import urllib.parse as urlp

# === important!! ===
router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/rainfall")
def get_rainfall(
    start_date: str = Query(..., description="Date de début au format YYYY-MM-DD"),
    end_date: str = Query(..., description="Date de fin au format YYYY-MM-DD"),
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude")
):
    # test simple
    return {
        "message": "Rainfall data requested successfully",
        "params": {
            "start_date": start_date,
            "end_date": end_date,
            "latitude": latitude,
            "longitude": longitude
        }
    }
