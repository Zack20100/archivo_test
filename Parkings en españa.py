# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:02:41 2023

@author: zlech
"""

%reset -f 
 
import os
import requests
import pandas as pd
import folium
from geopy.distance import distance
from geopy.geocoders import Nominatim

# Punto de ubicación
latitude_loc = 43.296482
longitude_loc = -1.985127

# Inicializar geocodificador
geolocator = Nominatim(user_agent="my_app")

# Encuentra la dirección correspondiente a la posición 
location = geolocator.reverse(f"{latitude_loc}, {longitude_loc}")
print(location.address)

# Ubicaciones para buscar
Ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Málaga", "Murcia", "Palma", "Las Palmas de Gran Canaria", "Bilbao", "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón", "L'Hospitalet de Llobregat", "La Coruña", "Granada", "Vitoria-Gasteiz", "Elche", "Santa Cruz de Tenerife", "Badalona", "Oviedo", "Móstoles", "Cartagena", "Terrassa", "Jerez de la Frontera", "Sabadell", "Alcalá de Henares", "Pamplona", "Donostia - San Sebastián", "Fuenlabrada", "Almería", "Leganés", "Santander", "Castellón de la Plana", "Burgos", "Albacete", "Getafe", "Níjar", "San Cristóbal de La Laguna", "Logroño", "Badajoz", "Salamanca", "Huelva", "Marbella", "Lleida", "Tarragona", "Dos Hermanas", "Torrejón de Ardoz", "Parla", "Mataró", "León", "Algeciras", "Santa Lucía de Tirajana", "Alcobendas", "Cádiz", "Reus", "Jaén", "Ourense", "Telde", "Barakaldo", "Santiago de Compostela", "Lugo", "Gerona", "Coslada", "Torrevieja", "Pontevedra", "Toledo", "Roquetas de Mar", "Guadalajara", "Torrent", "Chiclana de la Frontera", "Rivas-Vaciamadrid", "Sagunto", "Sant Boi de Llobregat", "Ceuta", "Manresa", "Ciudad Real", "Mijas", "Majadahonda", "Ribeira", "Arona", "Vilanova i la Geltrú", "El Puerto de Santa María", "Pinto", "Elda", "Ontinyent", "Ávila", "Irun", "Villena", "Puerto del Rosario", "Béjar", "Culleredo", "San Bartolomé de Tirajana", "Tarifa", "San Vicente del Raspeig", "Ronda", "Linares", "Viladecans"]

# Crear un DataFrame para almacenar los resultados
columns = ["Ciudades", "Nom", "Latitude", "Longitude", "Distance"]
df = pd.DataFrame(columns=columns)

# Crear un mapa con folium
map = folium.Map(location=[latitude_loc, longitude_loc], zoom_start=6)

# Buscar estacionamientos para cada ubicación
for Ciudades in Ciudades:
    # Construir la consulta Overpass
    query = f"""
    [out:json];
    area[name="{Ciudades}"]->.searchArea;
    area[name="España"]->.pais;
    node["amenity"="parking"](area.searchArea)(area.pais);
    out center;
    """
    
    # Realizar la solicitud de paso elevado con solicitudes
    url = "https://overpass-api.de/api/interpreter"
    params = {"data": query}
    response = requests.get(url, params=params)
    data = response.json()
    
    # Agregue los resultados de búsqueda para cada Ciudades en el DataFrame y el mapa
    for element in data["elements"]:
        name = element["tags"]["name"] if "name" in element["tags"] else "Inconnu"
        lat, lon = element['lat'], element['lon']
        parking_loc = (lat, lon)
        dist = distance(parking_loc, (latitude_loc, longitude_loc)).km
        
        df = df.append({"Ciudades": Ciudades, "Nom": name, "Latitude": lat, "Longitude": lon, "Distance": dist}, ignore_index=True)

        # Agregue un marcador para cada estacionamiento en el mapa
        folium.Marker(location=parking_loc, popup=f"{Ciudades} - {name}").add_to(map)

# Mostrar el marco de datos
print(df)


# Ruta de la carpeta para guardar el mapa
path = "Maps/"  

# Comprobar si existe la carpeta, si no crearla
if not os.path.exists(path):
    os.mkdir(path)

# Guarde el mapa en un archivo HTML y ábralo en el navegador
map.save(os.path.join(path, f"{Ciudades}.html"))
os.system(f"start {path}/{Ciudades}.html")