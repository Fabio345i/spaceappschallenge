from fastapi import APIRouter
from api.models import SubsetRequest
from api.utils.gesdisc_api import submit_and_wait, nc_to_json

router = APIRouter()

DATASET_ID = "M2T1NXSLV_5.12.4"

@router.post("/subset")
def merra2_subset(req: SubsetRequest):
    subset_req = {
        "methodname": "subset",
        "type": "jsonwsp/request",
        "version": "1.0",
        "args": {
            "role": "subset",
            "start": req.start,
            "end": req.end,
            "box": [req.minlon, req.minlat, req.maxlon, req.maxlat],
            "crop": True,
            "data": [
                {"datasetId": DATASET_ID, "variable": v}
                for v in req.variables
            ]
        }
    }
    urls = submit_and_wait(subset_req)

    nc_urls = [u for u in urls if u.endswith(".nc4") or ".nc4" in u]
    if not nc_urls:
        return {"urls": urls, "data": []}

    json_data = nc_to_json(nc_urls[0])
    return {"urls": urls, "data": json_data}

