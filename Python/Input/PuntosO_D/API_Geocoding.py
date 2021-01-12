
import os
import numpy as np
import pandas as pd
import requests

API_KEY = '#####################################'

# Importo el csv con los puntos de cada ciudad de provincia
df= pd.read_csv('/home/tfm/Escritorio/TFM/Datasets/direcciones_ciudades.csv', sep=';', encoding='unicode_escape', header=0)
lista = df.ADDRESS.tolist()


direccion = []
for ciudad in lista:
    params = {
    'key': API_KEY,
    'address': ciudad
    }
    direccion.append(params)
    print(direccion)
print()

direccion


base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'


# coordenadas = []
# for i in direccion:
#     response = requests.get(base_url, params=i).json()
#     #response.keys()

#     if response['status'] == 'OK':
#         geometry = response['results'][0]['geometry']
#         lat = geometry['location']['lat']
#         lon = geometry['location']['lng']
#         coordenadas.extend((lat,lon))
# print(coordenadas)

coordenadas_lat = []
coordenadas_long = []
for i in direccion:
    response = requests.get(base_url, params=i).json()
    #response.keys()

    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        lat = geometry['location']['lat']
        lon = geometry['location']['lng']
        coordenadas_lat.append(lat)
        coordenadas_long.append(lon)
print(coordenadas_lat, coordenadas_long)


# Incorporamos una columna latitud y una longitud al dataframe original
df['LATITUD'] = coordenadas_lat
df['LONGITUD'] = coordenadas_long
df

# Concatenamos la latitud y longitud en una sola columna nombrada como 'COORDENADAS'
df['COORDENADAS'] = df ['LATITUD']. map (str) + ',' + df ['LONGITUD']. map (str) 
df

# Renombro la columna PROVINCIA (etiquetada erroneamente)
df= df.rename(columns={'PROVINCIA': 'CAPITAL DE PROVINCIA'})


# Escribimos el dataframe final en un csv
df.to_csv('ciudades.csv', index=False)

