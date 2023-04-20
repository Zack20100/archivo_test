# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:22:26 2023

@author: zlech
"""

import os
import requests
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from geopy.distance import distance

# Pida al usuario que ingrese un país y una ciudad
pays = input("Entrez le nom du pays : ")
ville = input("Entrez le nom de la ville : ") 

# Convierta la ciudad en coordenadas geográficas con la API de geocodificación de Nominatim 
geolocator = Nominatim(user_agent="my_app")
location = geolocator.geocode(f"{ville}, {pays}")
if location is None:
    print("Ville non trouvée")
    exit()
latitude_loc, longitude_loc = location.latitude, location.longitude

# Cree la consulta para buscar playas en la ciudad especificada con la API de TomTom
url = f"https://api.tomtom.com/search/2/poiSearch/beach.json?key=chAXsTA3QB15oIFryZtIU8e5m8SRtsmJ&lat={latitude_loc}&lon={longitude_loc}&radius=10000"

# Enviar consulta y recuperar resultados 
response = requests.get(url)
data = response.json()

# Crea un DataFrame vacío para almacenar los resultados
df = pd.DataFrame(columns=["Ville", "Nom", "Latitude", "Longitude", "Distance"])

# Crear un mapa centrado en la ciudad
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=14)

# Agregar marcador para la posición del usuario
folium.Marker(location=[latitude_loc, longitude_loc], popup=f"Vous êtes ici ({ville})").add_to(map)

# Agregue un marcador para cada rango en el mapa y almacene los resultados en el DataFrame
for result in data["results"]:
    name = result["poi"]["name"] if "name" in result["poi"] else "Inconnu"
    lat, lon = result["position"]["lat"], result["position"]["lon"]
    beach_loc = (lat, lon)
    dist = distance(beach_loc, (latitude_loc, longitude_loc)).km

    df = df.append({"Ville": ville, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

    folium.Marker(location=beach_loc, popup=f"{name} ({dist:.2f} km)").add_to(map)

# Mostrar el marco de datos
print(df)

# Crear la carpeta para almacenar el mapa si no existe
path = "Maps/"
if not os.path.exists(path):
    os.mkdir(path)

# Guarde el mapa en un archivo HTML y ábralo en el navegador
map.save(os.path.join(path, f"{ville}_{pays}_playas.html"))
os.system(f"start {path}/{ville}_{pays}_playas.html")
