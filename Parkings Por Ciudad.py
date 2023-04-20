# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:44:38 2023

@author: zlech
"""

%reset -f

import os
import requests
import pandas as pd
import folium
from geopy.distance import distance
from geopy.geocoders import Nominatim

# Preguntar al usuario por la ciudad
Ciudad = input("Introduzca una ciudad para buscar aparcamiento: ")
print("Has elegido la ciudad de", Ciudad)

# Convertir ciudad a coordenadas geográficas
geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode(Ciudad)
if location is None:
    print("Ciudad no encontrada")
    exit()
latitude_loc, longitude_loc = location.latitude, location.longitude

# Cree la consulta Overpass para buscar parkins
query = f"""
[out:json];
area[name="{Ciudad}"]->.searchArea;
area[name="España"]->.pais;
node["amenity"="parking"](area.searchArea)(area.pais);
out center;
"""

# Envíe la consulta Overpass y recupere los resultados
response = requests.get(f"https://overpass-api.de/api/interpreter?data={query}")
data = response.json()

# Extrae las coordenadas de los parkins encontrados
parking_coords = []
for element in data["elements"]:
    if element["type"] == "node":
        lat = element["lat"]
        lon = element["lon"]
        parking_coords.append((lat, lon))

# Calcula la distancia entre la ciudad y cada estacionamiento encontrado
parking_distances = []
for coords in parking_coords:
    parking_loc = (coords[0], coords[1])
    dist = distance((latitude_loc, longitude_loc), parking_loc).km
    parking_distances.append(dist)

# Crear un DataFrame con las coordenadas y distancias de los estacionamientos encontrados
parking_data = pd.DataFrame({"latitude": [coords[0] for coords in parking_coords],
                             "longitude": [coords[1] for coords in parking_coords],
                             "distance": parking_distances})

# Crear un mapa con folium
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=13)

# Agregue un marcador para la posición actual en el mapa
folium.Marker(location=[latitude_loc, longitude_loc], popup=f"Vous êtes ici ({Ciudad})").add_to(map)

# Crea un DataFrame vacío para almacenar los resultados
df = pd.DataFrame(columns=["Ciudad", "Nom", "Latitude", "Longitude", "Distance"])

# Agregue un marcador para cada estacionamiento en el mapa y almacene los resultados en el DataFrame
for element in data["elements"]:
    if element["type"] == "node" and "amenity" in element["tags"] and element["tags"]["amenity"] == "parking":
        name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
        lat, lon = element['lat'], element['lon']
        parking_loc = (lat, lon)
        dist = distance(parking_loc, (latitude_loc, longitude_loc)).km
        
        df = df.append({"Ciudad": Ciudad, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

        folium.Marker(location=parking_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)

# Mostrar el DataFrame
print(df)

# Crear la carpeta para almacenar el mapa si no existe
path = "Maps/"  
if not os.path.exists(path):
    os.mkdir(path)

# Guarde el mapa en un archivo HTML y ábralo en el navegador
map.save(os.path.join(path, f"{Ciudad}.html"))
os.system(f"start {path}/{Ciudad}.html")
