from fastapi import APIRouter, Query, HTTPException
import requests

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/rainfall")
def get_rainfall(
    lat: float = Query(..., description="Latitude du point"),
    lon: float = Query(..., description="Longitude du point"),
    start: str = Query(..., regex=r"^\d{8}$", description="Date début YYYYMMDD"),
    end: str = Query(..., regex=r"^\d{8}$", description="Date fin YYYYMMDD"),
):
    """
    Récupère la pluie quotidienne NASA POWER pour un point entre start et end.
    """
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=PRECTOTCORR&start={start}&end={end}"
        f"&latitude={lat}&longitude={lon}&community=RE&format=JSON"
    )

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erreur lors de l'appel NASA POWER : {str(e)}")

    parameters = data.get("properties", {}).get("parameter", {})
    if not parameters or "PRECTOTCORR" not in parameters:
        raise HTTPException(status_code=500, detail="Aucune donnée de précipitation disponible pour ces dates/coordonnées")

    return {
        "start_date": start,
        "end_date": end,
        "latitude": lat,
        "longitude": lon,
        "data": parameters["PRECTOTCORR"]
    }