# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:49:39 2023

@author: zlech
"""

%reset -f

import json
import os
import requests
import pandas as pd
import folium
from geopy.distance import distance
from geopy.geocoders import Nominatim

# Demander à l'utilisateur de saisir une ville
Ciudad = input("Introduzca una ciudad para buscar una playa: ")
print("Has elegido la ciudad de", Ciudad)

# Convertir la ville en coordonnées géographiques
geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode(Ciudad)
if location is None:
    print("Ciudad no encontrada")
    exit()
latitude_loc, longitude_loc = location.latitude, location.longitude

# Créer la requête Overpass pour rechercher les plages
query = f"""
[out:json];
area[name="{Ciudad}"]->.searchArea;
area[name="España"]->.pais;
(
    node"natural"="beach"(area.pais);
);
out center;
"""

# Envoyer la requête Overpass et récupérer les résultats
response = requests.get(f"https://overpass-api.de/api/interpreter?data={query}")
if response.ok and response.status_code == 200:
    try:
        data = response.json()
    except json.decoder.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e.msg}")
        print(f"Contenu de la réponse : {response.content}")
        exit()
else:
    print(f"Erreur lors de la requête : {response.status_code}")
    exit()

# Exemple de coordonnées de plages
beach_coords = [(43.6045, 1.4440), (43.4914, 1.2171), (43.5271, 1.3148)]

# Coordonnées de l'emplacement actuel
latitude_loc = 43.5789
longitude_loc = 1.4416

beach_distances = []
for coords in beach_coords:
    beach_loc = (coords[0], coords[1])
    dist = distance((latitude_loc, longitude_loc), beach_loc).km
    beach_distances.append(dist)

# Créer un DataFrame avec les coordonnées et distances des plages trouvées
beach_data = pd.DataFrame({"latitude": [coords[0] for coords in beach_coords],
                           "longitude": [coords[1] for coords in beach_coords],
                           "distance": beach_distances})

# Créer une carte avec folium# Créer une carte centrée sur la ville
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=13)

# Ajouter un marqueur pour la position de l'utilisateur
folium.Marker(location=[latitude_loc, longitude_loc], popup=f"Vous êtes ici ({Ciudad})").add_to(map)

# Créer un DataFrame vide pour stocker les résultats
df = pd.DataFrame(columns=["Ciudad", "Nom", "Latitude", "Longitude", "Distance"])

# Ajouter un marqueur pour chaque plage sur la carte et stocker les résultats dans le DataFrame
for element in data["elements"]:
    if element["type"] == "node" and "natural" in element["tags"] and element["tags"]["natural"] == "beach":
        name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
        lat, lon = element['lat'], element['lon']
        beach_loc = (lat, lon)
        dist = distance(beach_loc, (latitude_loc, longitude_loc)).km

        df = df.append({"Ciudad": Ciudad, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

        folium.Marker(location=beach_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)

# Afficher le DataFrame
print(df)

# Créer le dossier pour stocker la carte si n'existe pas
path = "Maps/"
if not os.path.exists(path):
    os.mkdir(path)

# Enregistrer la carte dans un fichier HTML et l'ouvrir dans le navigateur
map.save(os.path.join(path, f"{Ciudad}_playas.html"))
os.system(f"start {path}/{Ciudad}_playas.html")