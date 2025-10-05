import requests
from models import DonnerMontagne


def Calculer_Point(name):
    url = f"https://nominatim.openstreetmap.org/search?q={name}&format=json"
    reponse_api = requests.get(url)
    donnee = reponse_api.json()

    if(donnee):
        latitude = float(donnee[0]['lat'])
        longitude = float(donnee[0]['lon'])
        return latitude, longitude
    else:
        return None, None


def CaculerDonnerMontagne(montagne: DonnerMontagne):

    # méthode qui trouve la altitude et la longitude de la montagne en fonctione de son nom
    latitude, longitude = Calculer_Point(montagne.name)

    # Je vais devoir récupérer les données de L'API SAM
    montagne.altitude_base = None
    montagne.altitude_sommet = None
    montagne.temperature_base = None
    montagne.humiditer_base = None
    montagne.vent_base = None
    montagne.precipitation_base = None

    # Calculer les données

    Δh = montagne.altitude_sommet - montagne.altitude_base

    # Plus tu monte en altitude plus la pression diminue, l'aire se dilate et la température baisse.
    humiditer_concentration = None
    if( montagne.humiditer_base > 80):
        humiditer_concentration = 9.8
    else:
        humiditer_concentration = 6.0

    # Température au sommet est altéré par la concentration de l'humidité = > formule de calcul
    montagne.temperature_sommet = montagne.temperature_base - humiditer_concentration(Δh / 1000)

    # Calculer le vent au sommet de la montagne
    montagne.vent_sommet = montagne.vent_base * (1 + 0.2 (Δh / 1000))

    # Précipitation Sommet
    montagne.premcipitation_sommet = montagne.precipitation_base * (1 + 0.1(Δh / 1000))


    return montagne