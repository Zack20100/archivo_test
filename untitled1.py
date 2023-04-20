# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:21:37 2023

@author: zlech
"""

# It's nice to be important, but, it's more important to be nice 


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

os.chdir(r"C:\Users\zlech\OneDrive\Documentos\Exam")

df1 = pd.read_csv("Real-life.csv", sep=",", encoding='latin-1')

df1.columns = ['Brand', 'Price', 'Body', 'Mileage', 'EngineV', 'Engine Type',
       'Registration', 'Year', 'Model']

#Obtener un breve resumen estadístico. 

for i in df1:
    print(df1[i].describe())

descripcion = df1.describe().T


#Comprobar la tipología los datos

df1.dtypes

df1.info()

# Analizar la variable Brand :
    
df1['Brand'].describe().T

#Veamos cuántas ventas hubo para cada marca.

df1.Brand.value_counts()

## Crear un gráfico de dispersión

plt.scatter(df1['Brand'], df1['Price'], s=df1['Year'], alpha=0.5, c=df1['Year'])
plt.xticks(rotation=45)
plt.xlabel('Marca')
plt.ylabel('Precio')
plt.title('Relacion entre Marca,Precio y Año de produccion')
plt.show()


# Crear un gráfico de barras horizontales
plt.barh(df1['Brand'], df1['Price'], color='g')
plt.xticks(rotation=45)
plt.xlabel('Precio')
plt.ylabel('Marca')
plt.title('Precio de coche por Marca')
plt.show()

# Crear un diagrama de caja

df1.boxplot(column=['Price'], by='Brand')
plt.xticks(rotation=45)
plt.xlabel('Marca')
plt.ylabel('Precio')
plt.title('Distribución de precios de vehículos por marca')
plt.show()

#Veamos solo los BMW

df1.loc[df1.Brand == "BMW"].sort_values(["Year","Model"],ascending=False)


# Representación de la relación de dos variables
df1.plot(kind="scatter", x="Brand", y="Price", rot=-45)

# Mostramos un grafico de barras de las marcas de coches :
    
df1["Brand"].value_counts().plot(x="Brand", y='frecuncia', kind='bar',
                                  legend=True, title="Marcas de coches")

# Mostramos un grafico de barras de los typos de coches :
    
df1["Engine Type"].value_counts().plot(x="Engine Type", y='frecuncia', kind='bar',
                                  legend=True, title="Typos de coches")

# Mostramos un grafico de barras de las marcas de coches :
    
df1["Body"].value_counts().plot(x="Body", y='frecuncia', kind='bar',
                                  legend=True, title="Typos de coches")

# Histograma :
    
df1.hist(column="Year")


sns.boxplot(x=df1["Brand"], y=df1["Price"])
plt.xticks(rotation=45)

sns.boxplot(x=df1["Brand"], y=df1["Year"])
plt.xticks(rotation=45)

sns.distplot(df1['Price'])
