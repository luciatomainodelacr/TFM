# =============================================================================
#  MATRIZ DE DISTANCIAS ENTRE LOS PUNTOS DE RECARGAS
# =============================================================================


"""
    Fuente: https://medium.com/how-to-use-google-distance-matrix-api-in-python/how-to-use-google-distance-matrix-api-in-python-ef9cd895303c

    Proceso: Mediande la API Google Distance Matrix se calculan las distancias entre 
    las ciudades y todos los puntos del conjunto: ciudades, puntos de recarga y
    gasolineras.

    1- Clave API en google cloud
    2- Carga de inputs y se apendizan los 3 dataframes
    3- Mediante un bucle que recorre todas las combinaciones existentes entre las 
    variables origen y destino, se hacen llamadas a la api de google para calcular
    las distancias.
    4- Se crea el dataframe final
    5- Se exporta el dataframe a un fichero .csv

    Notas: Es necesario crear una API Key en Google Cloud para ejecutarlo

    Inputs:
        - /home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI/ciudades.csv
        - /home/tfm/Documentos/TFM/Datasets/PuntosRecarga/puntos_carga_reduced_Espana.csv
        - /home/tfm/Documentos/TFM/Datasets/Gasolineras/gasolineras_reduced_Espana.csv

    Output: ciudades_distancia.csv
"""


# Se cargan las librerias
import pandas as pd

import matplotlib.pyplot as plt
import os
import googlemaps
from itertools import tee


# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/')


# API Google
API_key = '############################'
gmaps = googlemaps.Client(key=API_key)



# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

# Ciudades
df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'PuntosO_D/GeocodingAPI/ciudades.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')

# Puntos de recarga
df_ptos_recarga = pd.read_csv(os.path.join(os.getcwd(),'PuntosRecarga/puntos_carga_reduced_Espana.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')

# Gasolineras
df_gasolineras = pd.read_csv(os.path.join(os.getcwd(),'Gasolineras/gasolineras_reduced_Espana.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')



# 2.- Apendizar los tres dataframes -------------------------------
#------------------------------------------------------------------

# Se filtran las columnas necesarias
df_ciudades = df_ciudades[["id", "PROVINCIA", "ADDRESS", "Latitude", "Longitude"]]
df_ptos_recarga = df_ptos_recarga[["id", "province", "formatted_address", "latitude", "longitude"]]
df_gasolineras = df_gasolineras[["id", "provincia", "direccion", "latitud", "longitud"]] 


# Se renombran las columnas
df_ptos_recarga.columns = df_ciudades.columns
df_gasolineras.columns = df_ciudades.columns


# Se apendizan los dataframes
df_ciudades = df_ciudades.append(df_ptos_recarga)
df_ciudades = df_ciudades.append(df_gasolineras)


# Backup 
df = df_ptos_recarga.append(df_gasolineras)
# df_aux = df
df


"""
    PRUEBAS
"""


df_aux = pd.read_csv(os.path.join(os.getcwd(),'puntos_kk.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')

# Elimamos duplicados (comprobación)
df.drop_duplicates()





# 3.- Calculo Distancias -----------------------------------------
#------------------------------------------------------------------

# Funcion Pairwise
def pairwise(iterable):

    """"
    Construye iteraciones entre dos filas consecutivas)
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)



# Se inicializa una lista vacia para calcular las distancias
list_distancia = [0]
list_duracion = [0]
list_origen = []
list_destino = []


# Bucle que recorre cada par de filas y calcula la distancia
for (i1_aux, row1_aux), (i2_aux, row2_aux) in pairwise(df_aux.iterrows()):
      
      # Se asigna la latitud y longitud del punto de origen
      LatOrigin = row1_aux['Latitude'] 
      LongOrigin = row1_aux['Longitude']
      ciudad_ori = row1_aux['id']
      origins = (LatOrigin,LongOrigin)
      
      for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
                      
            # Se asigna la latitud y longitud de la fila siguiente
            LatDest = row1['Latitude']
            LongDest = row1['Longitude']
            ciudad_dest = row1['id']
            destination = (LatDest,LongDest)
            
            if (ciudad_ori != ciudad_dest):
                
                # Se llama a la funcion distance_matrix de google
                result_distance = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
                result_time_s = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]["duration"]["value"]
                
                # Se apendiza el resultado a la lista de distancias
                list_distancia.append(result_distance)
                list_duracion.append(result_time_s)
                list_origen.append(ciudad_ori)
                list_destino.append(ciudad_dest)



# 4.- Dataframe Distancias ----------------------------------------
#------------------------------------------------------------------

# Se elimina el primer elemento de la lista de distancias (inicializada con 0)
list_distancia.remove(0)
list_duracion.remove(0)

# Se crea el dataframe con las distancias
df_distancias = pd.DataFrame()

df_distancias['Origen'] = list_origen
df_distancias['Destino'] = list_destino
df_distancias['Distance_m'] = list_distancia
df_distancias['Distance_km'] = df_distancias['Distance_m']/1000
df_distancias['Duracion_seg'] = list_duracion
df_distancias['Duracion_min'] = df_distancias['Duracion_seg']/60



# 5.- Output ------------------------------------------------------
#------------------------------------------------------------------

df_distancias.to_csv('/home/tfm/Documentos/TFM/Datasets/Matriz_Distancias/_bu/matriz_distancia_v2.csv', sep = ";", index = False)


df.to_csv('/home/tfm/Documentos/TFM/Datasets/Matriz_Distancias/matriz_distancia_input.csv', sep = ";", index = False)


"""
    PRUEBAS
"""

df1 = pd.read_csv(os.path.join(os.getcwd(),'Matriz_Distancias/pruebas_google_api/_bu/matriz_distancia_v1.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')
df2 = pd.read_csv(os.path.join(os.getcwd(),'Matriz_Distancias/pruebas_google_api/_bu/matriz_distancia_v2.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')

df1 = df1.append(df2) 

del(d2)

len(df1)

