# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:36:46 2023

@author: zlech
"""

%reset -f

import os
import requests
import pandas as pd
import folium
from geopy.distance import distance
from geopy.geocoders import Nominatim

Preguntar al usuario por la ciudad
Ciudad = input("Introduzca una ciudad para buscar playa: ")
print("Has elegido la ciudad de", Ciudad)

Convertir ciudad a coordenadas geográficas
geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode(Ciudad)
if location is None:
print("Ciudad no encontrada")
exit()
latitude_loc, longitude_loc = location.latitude, location.longitude

Cree la consulta Overpass para buscar playas
query = f"""
[out:json];
area[name="{Ciudad}"]->.searchArea;
area[name="España"]->.pais;
(
node"amenity"="parking"(area.pais);
node"natural"="beach"(area.pais);
);
out center;
"""

Envíe la consulta Overpass et récupère les résultats
response = requests.get(f"https://overpass-api.de/api/interpreter?data={query}")
data = response.json()

Extraire les coordonnées des plages trouvés
parking_beach_coords = []
for element in data["elements"]:
if element["type"] == "node":
lat = element["lat"]
lon = element["lon"]
beach_coords.append((lat, lon))

Calculer la distance entre la ville et chaque plage trouvé
beach_distances = []
for coords in beach_coords:
beach_loc = (coords[0], coords[1])
dist = distance((latitude_loc, longitude_loc), beach_loc).km
beach_distances.append(dist)

Créer un DataFrame avec les coordonnées et distances des plages trouvés
beach_data = pd.DataFrame({"latitude": [coords[0] for coords in beach_coords],
"longitude": [coords[1] for coords in beach_coords],
"distance": beach_distances})

Créer une carte avec folium
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=13)

Ajouter un marqueur pour la position actuelle sur la carte
folium.Marker(location=[latitude_loc, longitude_loc], popup=f"Vous êtes ici ({Ciudad})").add_to(map)

Créer un DataFrame vide pour stocker les résultats
df = pd.DataFrame(columns=["Ciudad", "Nom", "Latitude", "Longitude", "Distance"])

Ajouter un marqueur pour chaque parking ou plage sur la carte et stocker les résultats dans le DataFrame
for element in data["elements"]:
if element["type"] == "node" and "amenity" in element["tags"] and element["tags"]["amenity"] == "parking":
name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
lat, lon = element['lat'], element['lon']
parking_beach_loc = (lat, lon)
dist = distance(parking_beach_loc, (latitude_loc, longitude_loc)).km

    df = df.append({"Ciudad": Ciudad, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

    folium.Marker(location=parking_beach_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)
    
elif element["type"] == "node" and "natural" in element["tags"] and element["tags"]["natural"] == "beach":
    name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
    lat, lon = element['lat'], element['lon']
    parking_beach_loc = (lat, lon)
    dist = distance(parking_beach_loc, (latitude_loc, longitude_loc)).km
    
    df = df.append({"Ciudad": Ciudad, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

    folium.Marker(location=parking_beach_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)
Afficher le DataFrame
print(df)

Créer le dossier pour stocker la carte si n'existe pas
path = "Maps/"
if not os.path.exists(path):
os.mkdir(path)

Enregistrer la carte dans un fichier HTML et l'ouvrir dans le navigateur
map.save(os.path.join(path, f"{Ciudad}.html"))
os.system(f"start {path}/{Ciudad}.html")