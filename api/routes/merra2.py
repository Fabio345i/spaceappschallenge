from fastapi import APIRouter, Query, HTTPException
import requests
import requests

router = APIRouter()
@router.get("/power/daily")
def get_power_daily(
    lat: float = Query(..., description="Latitude du point d'intérêt"),
    lon: float = Query(..., description="Longitude du point d'intérêt"),
    start: str = Query(..., regex=r"^\d{8}$", description="Date début au format YYYYMMDD"),
    end: str = Query(..., regex=r"^\d{8}$", description="Date fin au format YYYYMMDD"),
):
    """
    Récupère les données journalières NASA POWER (T2M, T2M_MIN, T2M_MAX, RH2M, U2M, V2M, PS, PRECTOTCORR)
    pour un point (lat, lon) entre start et end.
    """
    params = "T2M,T2M_MIN,T2M_MAX,RH2M,U2M,V2M,PS,PRECTOTCORR"
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={params}&start={start}&end={end}"
        f"&latitude={lat}&longitude={lon}&community=RE&format=JSON"
    )

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erreur lors de l'appel NASA POWER : {str(e)}")
    
    if "properties" not in data or "parameter" not in data["properties"]:
        raise HTTPException(status_code=500, detail="Réponse NASA POWER inattendue")

    return {
        "parameters": data["properties"]["parameter"],
        "metadata": data.get("header", {})
    }
