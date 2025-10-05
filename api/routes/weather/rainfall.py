from fastapi import APIRouter, HTTPException, Query
import requests
import pandas as pd
import urllib.parse as urlp
import io

router = APIRouter(prefix="/weather", tags=["Weather"])

def get_time_series(start_date, end_date, latitude, longitude, variable="NLDAS2:NLDAS_FORA0125_H_v2.0:Rainf"):
    base_url = "https://hydro1.gesdisc.eosdis.nasa.gov/daac-bin/access/timeseries.cgi"

    query_parameters = {
        "variable": variable,
        "type": "asc2",
        "location": f"GEOM:POINT({longitude}, {latitude})",
        "startDate": start_date,
        "endDate": end_date,
    }

    full_url = base_url + "?" + "&".join([f"{key}={urlp.quote(str(value))}" for key, value in query_parameters.items()])

    try:
        response = requests.get(full_url, timeout=60)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="La requête NASA a expiré (timeout).")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erreur lors de la requête NASA : {e}")

    return response.text

def parse_time_series(ts_str):
    try:
        df = pd.read_table(
            io.StringIO(ts_str),
            sep="\t",
            names=["time", "data"],
            header=10,
            parse_dates=["time"],
            on_bad_lines="skip"
        )
        if df.empty:
            raise ValueError("Aucune donnée valide trouvée dans la réponse NASA.")
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de parsing des données NASA : {str(e)}")

@router.get("/rainfall")
def get_rainfall(
    start_date: str = Query(..., description="Date de début au format YYYY-MM-DD"),
    end_date: str = Query(..., description="Date de fin au format YYYY-MM-DD"),
    latitude: float = Query(..., description="Latitude du point d’observation"),
    longitude: float = Query(..., description="Longitude du point d’observation"),
    limit: int = Query(10, description="Nombre maximum de résultats à retourner")
):
    start_api = start_date + "T00"
    end_api = end_date + "T00"

    raw_data = get_time_series(start_api, end_api, latitude, longitude)
    df = parse_time_series(raw_data)

    daily = df.resample("D", on="time").sum().reset_index()

    limited = daily.head(limit)

    return {
        "location": {"latitude": latitude, "longitude": longitude},
        "start_date": start_date,
        "end_date": end_date,
        "count": len(limited),
        "data": limited.to_dict(orient="records")
    }
