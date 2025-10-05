from fastapi import APIRouter, Query, HTTPException
import httpx
import math
import asyncio
from datetime import datetime, timedelta
import requests
import statistics

router = APIRouter()

NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
PARAMS = "T2M,T2M_MIN,T2M_MAX,RH2M,U2M,V2M,PS,PRECTOTCORR"

async def fetch_power(client: httpx.AsyncClient, lat: float, lon: float, date: str):
    url = (
        f"{NASA_POWER_URL}?parameters={PARAMS}"
        f"&start={date}&end={date}"
        f"&latitude={lat}&longitude={lon}&community=RE&format=JSON"
    )
    r = await client.get(url, timeout=30)
    r.raise_for_status()
    d = r.json()
    if "properties" not in d or "parameter" not in d["properties"]:
        return None
    p = d["properties"]["parameter"]
    def val(k): return list(p.get(k, {}).values())[0] if k in p and p[k] else None
    return {
        "T2M": val("T2M"),
        "T2M_MIN": val("T2M_MIN"),
        "T2M_MAX": val("T2M_MAX"),
        "RH2M": val("RH2M"),
        "U2M": val("U2M"),
        "V2M": val("V2M"),
        "PS": val("PS"),
        "PRECTOTCORR": val("PRECTOTCORR"),
    }

@router.get("/daily/analyse")
async def analyse_day(
    lat: float = Query(..., description="Latitude du point d'intérêt"),
    lon: float = Query(..., description="Longitude du point d'intérêt"),
    day: int = Query(..., ge=1, le=31, description="Jour du mois (1-31)"),
    month: int = Query(..., ge=1, le=12, description="Mois (1-12)"),
    years: int = Query(20, ge=1, le=50, description="Nombre d'années d'historique à analyser"),
):
    """
    Analyse climatique simplifiée pour un jour/mois donné sur N années en arrière
    (moyenne T°, humidité, vent, pluie, pression avec ΔP).
    """
    current_year = datetime.now().year
    dates_main = [f"{y}{month:02d}{day:02d}" for y in range(current_year - years, current_year)]
    prev_day = (datetime(2000, month, day) - timedelta(days=1)).day
    dates_prev = [f"{y}{month:02d}{prev_day:02d}" for y in range(current_year - years, current_year)]

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[fetch_power(client, lat, lon, d) for d in dates_main],
            *[fetch_power(client, lat, lon, d) for d in dates_prev],
            return_exceptions=True
        )

    main_data = results[:len(dates_main)]
    prev_data = results[len(dates_main):]

    T, Tmin, Tmax, H, V, P, R = [], [], [], [], [], [], []
    deltaP = []

    for i in range(len(dates_main)):
        cur = main_data[i] if isinstance(main_data[i], dict) else None
        prev = prev_data[i] if isinstance(prev_data[i], dict) else None
        if not cur:
            continue

        if cur.get("T2M") is not None: T.append(cur["T2M"])
        if cur.get("T2M_MIN") is not None: Tmin.append(cur["T2M_MIN"])
        if cur.get("T2M_MAX") is not None: Tmax.append(cur["T2M_MAX"])
        if cur.get("RH2M") is not None: H.append(cur["RH2M"])
        if cur.get("U2M") is not None and cur.get("V2M") is not None:
            V.append(math.sqrt(cur["U2M"]**2 + cur["V2M"]**2))
        if cur.get("PS") is not None: P.append(cur["PS"])
        if cur.get("PRECTOTCORR") is not None: R.append(cur["PRECTOTCORR"])

        if cur.get("PS") is not None and prev and prev.get("PS") is not None:
            deltaP.append(cur["PS"] - prev["PS"])

    if not T:
        raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour ces paramètres")

    Tbase = sum(T) / len(T)
    Tmin_base = sum(Tmin) / len(Tmin) if Tmin else Tbase
    Tmax_base = sum(Tmax) / len(Tmax) if Tmax else Tbase
    Hmean = sum(H) / len(H) if H else None
    Vmean = sum(V) / len(V) if V else None
    Pmean = sum(P) / len(P) if P else None

    dP_mean = sum(deltaP)/len(deltaP) if deltaP else None

    Tmin_adj = Tmin_base
    Tmax_adj = Tmax_base

    if Hmean is not None:
        if Hmean > 70: Tmin_adj += 0.5
        elif Hmean < 30: Tmin_adj -= 0.5

    if Vmean is not None and Vmean > 10:
        Tmin_adj += 0.5

    return {
        "historique_annees": len(T),
        "T_moyenne": round(Tbase, 2),
        "Tmin_moyenne": round(Tmin_base, 2),
        "Tmax_moyenne": round(Tmax_base, 2),
        "Tmin_ajustee": round(Tmin_adj, 2),
        "Tmax_ajustee": round(Tmax_adj, 2),
        "humidite_moyenne": round(Hmean, 1) if Hmean else None,
        "vent_moyen_m_s": round(Vmean, 2) if Vmean else None,
        "pression_moy_kPa": round(Pmean, 2) if Pmean else None,
        "variation_pression_moy_kPa": round(dP_mean, 2) if dP_mean else None,

        "note": "Algorithme simplifié POWER (sans nuages/omega/T850/skin temp). ΔP basé sur jour-1 POWER."
    }

@router.get("/daily/predict")
def predict_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    day: int = Query(..., ge=1, le=31),
    month: int = Query(..., ge=1, le=12),
    base_years: int = Query(20),
    future_year: int = Query(...),
    window_days: int = Query(3)
):
    current_year = datetime.utcnow().year
    start_year = current_year - base_years
    start = (datetime(start_year, month, day) - timedelta(days=window_days)).strftime("%Y%m%d")
    end = (datetime(current_year - 1, month, day) + timedelta(days=window_days)).strftime("%Y%m%d")

    params = "T2M,T2M_MIN,T2M_MAX,RH2M,U2M,V2M,PS,PRECTOTCORR"
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={params}&start={start}&end={end}"
        f"&latitude={lat}&longitude={lon}&community=RE&format=JSON"
    )

    try:
        resp = requests.get(url, timeout=40)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erreur NASA POWER : {e}")

    if "properties" not in data or "parameter" not in data["properties"]:
        raise HTTPException(500, "Réponse POWER inattendue")

    p = data["properties"]["parameter"]

    def to_dict(key):
        return {datetime.strptime(k, "%Y%m%d"): v for k, v in p.get(key, {}).items()}

    t2m = to_dict("T2M")
    tmin = to_dict("T2M_MIN")
    tmax = to_dict("T2M_MAX")
    rh = to_dict("RH2M")
    u = to_dict("U2M")
    v = to_dict("V2M")
    ps = to_dict("PS")
    precip = to_dict("PRECTOTCORR")

    ref_dates = []
    for year in range(current_year - base_years, current_year):
        center = datetime(year, month, day)
        for d in range(-window_days, window_days + 1):
            ref_dates.append(center + timedelta(days=d))

    t2m_vals = [t2m[d] for d in ref_dates if d in t2m]
    tmin_vals = [tmin[d] for d in ref_dates if d in tmin]
    tmax_vals = [tmax[d] for d in ref_dates if d in tmax]
    rh_vals = [rh[d] for d in ref_dates if d in rh]
    u_vals = [u[d] for d in ref_dates if d in u]
    v_vals = [v[d] for d in ref_dates if d in v]
    ps_vals = [ps[d] for d in ref_dates if d in ps]


    if not t2m_vals:
        raise HTTPException(404, "Pas de données disponibles pour ce point/date")

    Tmean = sum(t2m_vals) / len(t2m_vals)
    Tmin = sum(tmin_vals) / len(tmin_vals) if tmin_vals else None
    Tmax = sum(tmax_vals) / len(tmax_vals) if tmax_vals else None
    RH = sum(rh_vals) / len(rh_vals) if rh_vals else None
    U = sum(u_vals) / len(u_vals) if u_vals else None
    V = sum(v_vals) / len(v_vals) if v_vals else None
    P = sum(ps_vals) / len(ps_vals) if ps_vals else None



    Tmin_adj = Tmin
    Tmax_adj = Tmax
    if RH:
        if RH > 70: Tmin_adj += 0.5
        elif RH < 30: Tmin_adj -= 0.5
    vent = None
    if U is not None and V is not None:
        vent = (U ** 2 + V ** 2) ** 0.5
        if vent > 10: Tmin_adj += 0.5

    return {
        "future_year": future_year,
        "date_predite": f"{future_year:04d}-{month:02d}-{day:02d}",
        "periode_utilisee": {
            "start": ref_dates[0].strftime("%Y-%m-%d"),
            "end": ref_dates[-1].strftime("%Y-%m-%d"),
            "nb_jours": len(ref_dates)
        },
        "T_moyenne": Tmean,
        "Tmin_base": Tmin,
        "Tmax_base": Tmax,
        "Tmin_ajustee": Tmin_adj,
        "Tmax_ajustee": Tmax_adj,
        "T2M_std": statistics.pstdev(t2m_vals) if len(t2m_vals) > 1 else None,
        "humidite_moyenne": RH,
        "vent_moyen_m_s": vent,
        "pression_moy_kPa": P,
    }
