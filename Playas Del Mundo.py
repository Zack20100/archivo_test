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

# Función para recuperar datos de la solicitud de Overpass
def overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': query})
    data = response.json()
    return data

# Pida al usuario que ingrese un país y una ciudad
pays = input("Entrez le nom du pays : ")
ville = input("Entrez le nom de la ville : ")

# Convertir ciudad a coordenadas geográficas
geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode(f"{ville}, {pays}")
if location is None:
    print("Ville non trouvée")
    exit()
latitude_loc, longitude_loc = location.latitude, location.longitude

# Cree la consulta Overpass para buscar playas en la ciudad especificada
query = f"""
[out:json];
area[name="{ville}"]->.searchArea;
area[name="{pays}"]->.country;
(
    node["natural"="beach"](area.searchArea);
);
out center;
"""

# Enviar consulta y recuperar resultados
data = overpass_query(query)

# Crea un DataFrame vacío para almacenar los resultados
df = pd.DataFrame(columns=["Ville", "Nom", "Latitude", "Longitude", "Distance"])

# Crear un mapa centrado en la ciudad
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=13)

# Agregar marcador para la posición del usuario
folium.Marker(location=[latitude_loc, longitude_loc], popup=f"Vous êtes ici ({ville})").add_to(map)

# Agregue un marcador para cada rango en el mapa y almacene los resultados en el DataFrame
for element in data["elements"]:
    if element["type"] == "node" and "natural" in element["tags"] and element["tags"]["natural"] == "beach":
        name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
        lat, lon = element['lat'], element['lon']
        beach_loc = (lat, lon)
        dist = distance(beach_loc, (latitude_loc, longitude_loc)).km

        df = df.append({"Ville": ville, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

        folium.Marker(location=beach_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)


# Mostrar el DataFrame
print(df)


# Crear la carpeta para almacenar el mapa si no existe
path = "Maps/"
if not os.path.exists(path):
    os.mkdir(path)

# Guarde el mapa en un archivo HTML y ábralo en el navegador
map.save(os.path.join(path, f"{pays}_playas.html"))
os.system(f"start {path}/{pays}_playas.html")