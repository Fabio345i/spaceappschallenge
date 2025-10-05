import requests

lat = 46.8
lon = -71.2
start = "20230225"   # YYYYMMDD
end = "20230225"

params = "T2M,T2M_MIN,T2M_MAX,RH2M,U2M,V2M,PS,PRECTOTCORR"
url = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    f"?parameters={params}"
    "&start=20230220&end=20230228"
    "&latitude=46.8&longitude=-71.2"
    "&community=RE&format=JSON"
)


resp = requests.get(url, timeout=30)
resp.raise_for_status()
data = resp.json()

# Les valeurs sont dans data["properties"]["parameter"]
params = data["properties"]["parameter"]
print(params)
