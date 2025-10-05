from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
import requests

router = APIRouter()
EONET = "https://eonet.gsfc.nasa.gov/api/v3/events"

def place_str(geom: dict) -> str | None:
    """Return '43.6°N, 79.4°W' from Point or Polygon; None if not available."""
    c, t = geom.get("coordinates"), geom.get("type")
    if not c: 
        return None
    if t == "Point" and isinstance(c, list) and len(c) >= 2:
        lon, lat = c[0], c[1]
    elif t == "Polygon" and isinstance(c, list) and c and isinstance(c[0], list) and c[0]:
        xs = [p[0] for p in c[0]]
        ys = [p[1] for p in c[0]]
        lon, lat = sum(xs)/len(xs), sum(ys)/len(ys)
    else:
        return None
    return f"{abs(lat):.1f}°{'N' if lat>=0 else 'S'}, {abs(lon):.1f}°{'E' if lon>=0 else 'W'}"

@router.get("/disasters/headlines")
def disasters_headlines(
    date: str = Query(..., description="UTC date: YYYY-MM-DD"),
    limit: int = Query(50, ge=1, le=200, description="Max number of events"),
):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(400, "date must be YYYY-MM-DD")

    try:
        r = requests.get(EONET, params={"start": date, "end": date, "status": "all", "limit": 1000}, timeout=20)
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(502, f"EONET error: {e}")

    events = r.json().get("events", [])
    headlines = []

    for ev in events:
        title = ev.get("title") or "Event"
        cat = (ev.get("categories") or [{}])[0].get("title", "Event")

        geom = next((g for g in ev.get("geometry", []) if g.get("date", "").startswith(date)), None)
        if not geom:
            continue

        place = place_str(geom) or "location unavailable"
        headlines.append(f"{cat} — '{title}' — {place} — {date} (UTC)")

        if len(headlines) >= limit:
            break

    if not headlines:
        headlines = [f"No notable activity detected for {date} (UTC)"]

    return {"date": date, "headlines": headlines, "source": "NASA EONET"}
