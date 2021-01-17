# =============================================================================
#  MATRIZ DE DISTANCIAS ENTRE LOS PUNTOS DE RECARGAS
# =============================================================================

""" 
EL CALCULO SE HACE SOLO PARA FILAS ITERATIVAS
--> HACE FALTA CREAR LA MATRIZ PARA TODOS LOS PUNTOS
"""


# Se cargan las librerias
import pandas as pd
import matplotlib.pyplot as plt
import os
import googlemaps
from itertools import tee


# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI')



# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'ciudades.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')

# Backup 
df = df_ciudades
df_aux = df_ciudades
df



# 2.- Configuracion API Google ------------------------------------
#------------------------------------------------------------------

# La clave se introduce para la ejecucion pero luego se omitira para no compartirla en el repo
API_key = '#################################'
gmaps = googlemaps.Client(key=API_key)



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
list = [0]
list_origen = []
list_destino = []


# Bucle que recorre cada par de filas y calcula la distancia

for (i1_aux, row1_aux), (i2_aux, row2_aux) in pairwise(df_aux.iterrows()):
      
      # Se asigna la latitud y longitud del punto de origen
      LatOrigin = row1_aux['Latitude'] 
      LongOrigin = row1_aux['Longitude']
      ciudad_ori = row1_aux['CAPITAL DE PROVINCIA']
      origins = (LatOrigin,LongOrigin)
      
      for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
                      
            # Se asigna la latitud y longitud de la fila siguiente
            LatDest = row1['Latitude']
            LongDest = row1['Longitude']
            ciudad_dest = row1['CAPITAL DE PROVINCIA']
            destination = (LatDest,LongDest)
                        
            # Se llama a la funcion distance_matrix de google
            result = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
      
            # Se apendiza el resultado a la lista de distancias
            list.append(result)
            list_origen.append(ciudad_ori)
            list_destino.append(ciudad_dest)



# 4.- Dataframe Distancias ----------------------------------------
#------------------------------------------------------------------

# Se elimina el primer elemento de la lista de distancias (inicializada con 0)
list.remove(0)

# Se crea el dataframe con las distancias
df_distancias = pd.DataFrame()

df_distancias['Origen'] = list_origen
df_distancias['Destino'] = list_destino
df_distancias['Distance_m'] = list


df_distancias['Distance_km'] = df_distancias['Distance_m']/1000



# 5.- Output ------------------------------------------------------
#------------------------------------------------------------------

df_distancias.to_csv('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI/ciudades_distancia.csv', sep = ";", index = False)


