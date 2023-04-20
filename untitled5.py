# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 10:44:06 2023

@author: zlech
"""

%reset -f

import os
import requests
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.distance import distance

# Fonction pour récupérer les données de la requête Overpass
def overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    data = response.json()
    return data

# Demander à l'utilisateur de saisir un pays et une ville
pays = input("Entrez le nom du pays : ")
ville = input("Entrez le nom de la ville : ")

# Convertir la ville en coordonnées géographiques
geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode(f"{ville}, {pays}")
if location is None:
    print("Ville non trouvée")
    exit()
latitude_loc, longitude_loc = location.latitude, location.longitude

# Créer la requête Overpass pour rechercher les plages dans la ville spécifiée
query = f"""
[out:json];
area[name="{ville}"]->.searchArea;
area[name="{pays}"]->.country;
(
    node["natural"="beach"](area.searchArea);
);
out center;
"""

# Envoyer la requête Overpass et récupérer les résultats
data = overpass_query(query)

# Créer un DataFrame vide pour stocker les résultats
df = pd.DataFrame(columns=["Ville", "Nom", "Latitude", "Longitude", "Distance"])

# Créer une carte centrée sur la ville
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=13)

# Ajouter un marqueur pour la position de l'utilisateur
folium.Marker(location=[latitude_loc, longitude_loc], popup=f"Vous êtes ici ({ville})").add_to(map)

# Ajouter un marqueur pour chaque plage sur la carte et stocker les résultats dans le DataFrame
for element in data["elements"]:
    if element["type"] == "node" and "natural" in element["tags"] and element["tags"]["natural"] == "beach":
        name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
        lat, lon = element['lat'], element['lon']
        beach_loc = (lat, lon)
        dist = distance(beach_loc, (latitude_loc, longitude_loc)).km

        df = df.append({"Ville": ville, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

        folium.Marker(location=beach_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)


# Afficher le DataFrame
print(df)


# Créer le dossier pour stocker la carte si n'existe pas
path = "Maps/"
if not os.path.exists(path):
    os.mkdir(path)

# Enregistrer la carte dans un fichier HTML et l'ouvrir dans le navigateur
map.save(os.path.join(path, f"{ville}_playas.html"))
os.system(f"start {path}/{ville}_playas.html")