# =============================================================================
# DESCARGA DATOS CIUDADES (ORIGEN - DESTINO) - GOOGLE MAPS PLACES API
# =============================================================================


"""
    Proceso: 

    Input: 
        - /home/tfm/Documentos/TFM/Datasets/PuntosO_D/direcciones_ciudades.csv
    
    Output:
        - /home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI/ciudades.csv
 
"""

# Se cargan las librerias
import os
import numpy as np
import pandas as pd
import requests

# API Google
API_KEY = '#####################################'



# 1.- Carga de datos inputs ---------------------------------------
#------------------------------------------------------------------

# Importo el csv con los puntos de cada ciudad de provincia
df = pd.read_csv('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/direcciones_ciudades.csv', sep=',', encoding='unicode_escape', header=0)

# Lista con las direcciones de las distintas ciudades
lista = df.Direccion.tolist()


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
df["Latitud"]   = coordenadas_lat
df["Longitud"]  = coordenadas_long
df

# Concatenamos la latitud y longitud en una sola columna nombrada como 'COORDENADAS'
df["Coordenadas"] = df["Latitud"].map(str) + ',' + df["Longitud"].map(str) 
df



# 3.- Output ------------------------------------------------------
#------------------------------------------------------------------

df.to_csv('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI/ciudades.csv', index = False)

