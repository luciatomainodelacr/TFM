# =============================================================================
#  MATRIZ DE DISTANCIAS ENTRE LOS PUNTOS DE RECARGAS
# =============================================================================

"""
¡! SOLO FUNCIONA PARA POCOS PUNTOS - NO ES OPTIMO PARA EL CASO CON EL QUE SE 
ESTA TRABAJANDO

--> SE UTILIZA MEJOR LA API DE GOOGLE PARA MATRIZ DE DISTANCIAS
matriz_distancias_api_google.py

"""

# Se cargan las librerias
import math
import pandas as pd
import os

# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Python/Modelo/')



# 1.- Funciones auxiliares ----------------------------------------
#------------------------------------------------------------------

# Distancia Haversine
def haversine(lat1, lon1, lat2, lon2):
    """
        Calcula la distancia Haversine de dos puntos
        dados
    """
    rad = math.pi/180
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    R = 6372.795477598
    a = (math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia = 2*R*math.asin(math.sqrt(a))
    return distancia


# Función Potencia
def potencia(c):
    """
        Calcula y devuelve el conjunto potencia del 
        conjunto c.
    """
    if len(c) == 0:
        return [[]]
    r = potencia(c[:-1])
    return r + [s + [c[-1]] for s in r]


# Función Combinaciones
def combinaciones(c, n):
    """Calcula y devuelve una lista con todas las
       combinaciones posibles que se pueden hacer
       con los elementos contenidos en c tomando n
       elementos a la vez.
    """
    return [s for s in potencia(c) if len(s) == n]


# Función imprime_ordenado
def imprime_ordenado(c):
    """Imprime en la salida estándar todos los
       subconjuntos del conjunto c (una lista de
       listas) ordenados primero por tamaño y
       luego lexicográficamente. Cada subconjunto
       se imprime en su propia línea. Los
       elementos de los subconjuntos deben ser
       comparables entre sí, de otra forma puede
       ocurrir un TypeError.
    """
    for e in sorted(c, key=lambda s: (len(s), s)):
        print(e)


# 2.- Carga de datos inputs ---------------------------------------
#------------------------------------------------------------------


# Se lee el fichero con los puntos de carga electrica
df_ptos = pd.read_csv(os.path.join(os.getcwd(),'nodes.csv'), sep=',', encoding='iso-8859-1', decimal='.')





# 3.- Construcción de la matriz -----------------------------------
#------------------------------------------------------------------


ptos_unicos = df_ptos["puntos"].unique()
ptos_combinacion = combinaciones(ptos_unicos, 2)


# Se genera el dataframe de combinatorias de puntos
df_results = pd.DataFrame(columns= ["origen", "destino", "distancia"], index = range(len(ptos_combinacion)))

for i in df_results.index:
    df_results["origen"][i] = ptos_combinacion[i][0]
    df_results["destino"][i] = ptos_combinacion[i][1]

df_results


# Se calcula la distancia para cada par de puntos
for i in df_results.index:
    lat_1 = df_ptos[df_ptos['puntos'] == df_results["origen"][i]].latitude[df_ptos[df_ptos['puntos'] == df_results["origen"][i]].index[0]]
    long_1 = df_ptos[df_ptos['puntos'] == df_results["origen"][i]].longitude[df_ptos[df_ptos['puntos'] == df_results["origen"][i]].index[0]]
    lat_2 = df_ptos[df_ptos['puntos'] == df_results["destino"][i]].latitude[df_ptos[df_ptos['puntos'] == df_results["destino"][i]].index[0]]
    long_2 = df_ptos[df_ptos['puntos'] == df_results["destino"][i]].longitude[df_ptos[df_ptos['puntos'] == df_results["destino"][i]].index[0]]

    df_results["distancia"][i] = haversine(lat_1, long_1, lat_2, long_2)

df_results







