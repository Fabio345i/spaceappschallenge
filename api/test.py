import requests
from datetime import datetime

#  Fonction : récupère data et calcule la moyenne pluie
#
def get_average_precipitation(lat, lon, start_date, end_date):
    """
    Calcule la moyenne des précipitations (mm/jour) pour une période donnée.
    Utilise NASA POWER API (données journalières).
    """
    try:
        datetime.strptime(start_date, "%Y%m%d")
        datetime.strptime(end_date, "%Y%m%d")
    except ValueError:
        raise ValueError("Les dates doivent être au format YYYYMMDD (ex: 20250201).")

    params = "PRECTOTCORR"  
    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={params}"
        f"&start={start_date}&end={end_date}"
        f"&latitude={lat}&longitude={lon}"
        "&community=RE&format=JSON"
    )

    print(f"🔗 Requête NASA POWER : {url}")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(" Erreur de connexion à l'API NASA :", e)
        return None

    if "properties" not in data or "parameter" not in data["properties"]:
        print("Structure inattendue dans la réponse NASA.")
        return None

    params_data = data["properties"]["parameter"]
    rain_data = params_data.get("PRECTOTCORR", {})

    if not rain_data:
        print("Aucune donnée de précipitation trouvée pour cette période.")
        return None

    values = list(rain_data.values())
    avg_precip = sum(values) / len(values)
    print(f"Moyenne de précipitations du {start_date} au {end_date} : {avg_precip:.2f} mm/jour")

    return avg_precip


if __name__ == "__main__":
    print("=== Calcul de la moyenne des précipitations NASA POWER ===")

    lat = float(input("Latitude : "))
    lon = float(input("Longitude : "))
    start = input("Date de début (YYYYMMDD) : ")
    end = input("Date de fin (YYYYMMDD) : ")

    avg = get_average_precipitation(lat, lon, start, end)

    if avg is not None:
        print(f"\n✅ Résultat final : {avg:.2f} mm/jour en moyenne sur la période.")
