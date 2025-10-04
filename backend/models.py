
class DonnerMontagne:
    def __init__(self,name):


        # Donnée données part un utilisateur
        self.name = name

        # Donnée qui sont données part la création de Sam
        self.altitude_base = None
        self.altitude_sommet = None
        self.temperature_base = None
        self.humiditer_base = None
        self.vent_base = None
        self.precipitation_base = None

        # Données qui doivent etre calculer

        self.temperature_sommet = None
        self.vent_sommet = None
        self.premcipitation_sommet = None

    def __repr__(self):
           return f"<Microclimat {self.name} - Sommet {self.altitude_sommet}m>"
        
        
