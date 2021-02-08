# =============================================================================
#  MATRIZ DE DISTANCIAS ENTRE LOS PUNTOS DE RECARGAS
# =============================================================================

"""

Input: matriz_distancia_input.csv - contiene las coordenadas de las ciudades, 
        puntos de recarga y gasolineras

Proceso: Mediante funciones se calculan todas las combinaciones entre los distintos 
puntos del dataframe nodes y se calcula la distancia de Haversine entre ellos. 


Output: Devuelve un dataframe con las distancias para todas las combinaciones.
 
"""


# Se cargan las librerias
from itertools import tee
import math
import pandas as pd
import os


# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/')



# 1.- Funciones auxiliares ----------------------------------------
#------------------------------------------------------------------

# Distancia Haversine
def haversine(lat1, lon1, lat2, lon2):
     """
    Definicion de la funcion haversine:
        
        Funcion para calcular la distancia Haversine de dos
        puntos dados

    Parametros
    ----------
    lat1:                     float
        Float con la latitud del primer punto
        
    lon1:                     float
        Float con la longitud del primer punto
    
    lat2:                     float
        Float con la latitud del segundo punto
    
    lon2:                     float
        Float con la longitud del segundo punto
    
    Returns
    ------
    distancia:                float
        Float que contiene la distancia entre dos puntos
        definidos
    
    Ejemplo
    -------
    >>> result_distance = haversine(LatOrigin, LongOrigin, LatDest, LongDest)
    """
     rad         = math.pi/180
     dlat        = lat2 - lat1
     dlon        = lon2 - lon1
     R           = 6372.795477598
     a           = (math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
     distancia   = 2*R*math.asin(math.sqrt(a))

     return distancia


# Funcion Pairwise
def pairwise(iterable):
     """
    Definicion de la funcion pairwise:
        
        Funcion para construir iteraciones entre dos filas
        consecutivas 

    Parametros
    ----------
    iterable:                 iterable
        Iterador que recorre las filas de un Dataframe
    
    Returns
    ------
    zip(a, b):                tuple
        Tupla con clave, valor del Dataframe sobre el que 
        se itera
    
    Ejemplo
    -------
    >>> for (i1, row1), (i2, row2) in pairwise(df.iterrows())
    """
     a, b = tee(iterable)
     next(b, None)
     return zip(a, b)



# 2.- Carga de datos inputs ---------------------------------------
#------------------------------------------------------------------

# Se lee el fichero con los puntos de carga electrica
df      = pd.read_csv(os.path.join(os.getcwd(),'Matriz_Distancias/matriz_distancia_input.csv'), sep=';', encoding='iso-8859-1', decimal='.')
df_aux  = df



# 3.- Construcción de la matriz -----------------------------------
#------------------------------------------------------------------

# Se inicializa una lista vacia para calcular las distancias
list_origen     = []
list_destino    = []
list_distancia  = [0]

# Bucle que recorre cada par de filas y calcula la distancia
for (i1_aux, row1_aux), (i2_aux, row2_aux) in pairwise(df_aux.iterrows()):
      
      # Se asigna la latitud y longitud del punto de origen
      LatOrigin  = row1_aux["atitude"] 
      LongOrigin = row1_aux["Longitude"]
      ciudad_ori = row1_aux["id"]
      origins    = (LatOrigin,LongOrigin)
      
      for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
                      
            # Se asigna la latitud y longitud de la fila siguiente
            LatDest     = row1["Latitude"]
            LongDest    = row1["Longitude"]
            ciudad_dest = row1["id"]
            destination = (LatDest, LongDest)
            
            if (ciudad_ori != ciudad_dest):
                
                # Se llama a la funcion distance_matrix de google
                result_distance = haversine(LatOrigin, LongOrigin, LatDest, LongDest)
                
                # Se apendiza el resultado a la lista de distancias               
                list_origen.append(ciudad_ori)
                list_destino.append(ciudad_dest)
                list_distancia.append(result_distance) 



# 4.- Dataframe Distancias ----------------------------------------
#------------------------------------------------------------------

# Se elimina el primer elemento de la lista de distancias (inicializada con 0)
list_distancia.remove(0)


# Se crea el dataframe con las distancias
df_dist_haversine = pd.DataFrame()

df_dist_haversine["Origen"]      = list_origen
df_dist_haversine["Destino"]     = list_destino
df_dist_haversine["Distance_km"] = list_distancia



# 5.- Output ------------------------------------------------------
#------------------------------------------------------------------

df_dist_haversine.to_csv('/home/tfm/Documentos/TFM/Datasets/Matriz_Distancias/matriz_distancia_haversine.csv', sep = ";", index = False)



