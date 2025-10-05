import json
import time
import urllib3
import certifi
from fastapi import HTTPException
import xarray as xr
import tempfile
import requests
import numpy as np

GES_DISC_URL = "https://disc.gsfc.nasa.gov/service/subset/jsonwsp"
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())


def nc_to_json(url: str, minlat=None, maxlat=None, minlon=None, maxlon=None) -> list[dict]:
    clean_url = url.split("?")[0]

    with tempfile.NamedTemporaryFile(suffix=".nc4", delete=False) as tmp:
        local_path = tmp.name
    with requests.get(clean_url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    ds = xr.open_dataset(local_path)

    if minlat is not None and maxlat is not None:
        ds = ds.sel(lat=slice(minlat, maxlat))
    if minlon is not None and maxlon is not None:
        ds = ds.sel(lon=slice(minlon, maxlon))

    ds = ds.where(~xr.ufuncs.isnan(ds), other=np.nan)
    df = ds.to_dataframe().reset_index()
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")


def post_wsp(body: dict):
    r = http.request(
        "POST",
        GES_DISC_URL,
        body=json.dumps(body),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    resp = json.loads(r.data)
    if resp.get("type") == "jsonwsp/fault":
        raise HTTPException(status_code=500, detail=f"API error: {resp}")
    return resp


def submit_and_wait(subset_request: dict) -> list[str]:
    resp = post_wsp(subset_request)
    job_id = resp["result"]["jobId"]
    status = resp["result"]["Status"]

    status_req = {
        "methodname": "GetStatus",
        "version": "1.0",
        "type": "jsonwsp/request",
        "args": {"jobId": job_id},
    }
    while status in ["Accepted", "Running"]:
        time.sleep(5)
        resp = post_wsp(status_req)
        status = resp["result"]["Status"]
    if status != "Succeeded":
        raise HTTPException(status_code=500, detail=f"Job failed: {resp}")

    results_req = {
        "methodname": "GetResult",
        "version": "1.0",
        "type": "jsonwsp/request",
        "args": {"jobId": job_id, "count": 20, "startIndex": 0},
    }
    resp = post_wsp(results_req)
    items = resp["result"]["items"]
    urls = [i["link"] for i in items if "link" in i]
    return urls
