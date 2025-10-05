import json, time
import urllib3
import certifi
from fastapi import HTTPException
import xarray as xr
import os
import requests
GES_DISC_URL = "https://disc.gsfc.nasa.gov/service/subset/jsonwsp"
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def nc_to_json(url: str) -> list[dict]:
    import os, requests, xarray as xr

    clean_url = url.split("?")[0]
    user = os.getenv("EARTHDATA_USER")
    pwd = os.getenv("EARTHDATA_PASS")

    if not user or not pwd:
        raise RuntimeError("EARTHDATA_USER / EARTHDATA_PASS non définis")

    local_path = "/tmp/temp_merra2.nc4"
    with requests.get(clean_url, auth=(user, pwd), stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    ds = xr.open_dataset(local_path)
    df = ds.to_dataframe().reset_index()
    return df.to_dict(orient="records")


def post_wsp(body: dict):
    r = http.request("POST", GES_DISC_URL, body=json.dumps(body),
                     headers={"Content-Type": "application/json", "Accept": "application/json"})
    resp = json.loads(r.data)
    if resp.get("type") == "jsonwsp/fault":
        raise HTTPException(status_code=500, detail=f"API error: {resp}")
    return resp

def submit_and_wait(subset_request: dict) -> list[str]:
    # submit
    resp = post_wsp(subset_request)
    job_id = resp["result"]["jobId"]
    status = resp["result"]["Status"]

    # poll
    status_req = {
        "methodname": "GetStatus",
        "version": "1.0",
        "type": "jsonwsp/request",
        "args": {"jobId": job_id}
    }
    while status in ["Accepted", "Running"]:
        time.sleep(5)
        resp = post_wsp(status_req)
        status = resp["result"]["Status"]
    if status != "Succeeded":
        raise HTTPException(status_code=500, detail=f"Job failed: {resp}")

    # fetch results
    results_req = {
        "methodname": "GetResult",
        "version": "1.0",
        "type": "jsonwsp/request",
        "args": {"jobId": job_id, "count": 20, "startIndex": 0}
    }
    resp = post_wsp(results_req)
    items = resp["result"]["items"]
    return [i["link"] for i in items if "link" in i]
