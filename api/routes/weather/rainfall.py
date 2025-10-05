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

    response = requests.get(full_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Erreur API NASA : {response.text}")
    
    return response.text

def parse_time_series(ts_str):
    try:
        df = pd.read_table(io.StringIO(ts_str), sep="\t", names=["time", "data"], header=10, parse_dates=["time"])
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de parsing des données NASA : {str(e)}")

@router.get("/rainfall")
def get_rainfall(
    start_date: str = Query(..., description="Date de début au format YYYY-MM-DD"),
    end_date: str = Query(..., description="Date de fin au format YYYY-MM-DD"),
    latitude: float = Query(..., description="Latitude du point d’observation"),
    longitude: float = Query(..., description="Longitude du point d’observation")
):
    start_api = start_date + "T00"
    end_api = end_date + "T00"

    raw_data = get_time_series(start_api, end_api, latitude, longitude)

    df = parse_time_series(raw_data)

    daily = df.resample("D", on="time").sum().reset_index()

    return {"data": daily.to_dict(orient="records")}
