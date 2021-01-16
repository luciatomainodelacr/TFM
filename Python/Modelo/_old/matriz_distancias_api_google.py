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
os.chdir('/home/tfm/Documentos/TFM/Datasets/')



# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'ciudades.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')

# Backup 
df = df_ciudades
df



# 2.- Grafico mapa España -----------------------------------------
#------------------------------------------------------------------

espana = plt.imread("/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/GoogleMapsAPI/espana.png")
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df.LONGITUD, df.LATITUD, zorder = 1, alpha = 0.2, c = 'b', s = 10)
ax.set_title('Plotting Spatial Data on Spain Map')
ax.set_xlim(BBox[0], BBox[1])
ax.set_ylim(BBox[2], BBox[3])
ax.imshow(espana, zorder = 0, extent = BBox, aspect = 'equal')
# plt.show()

# --> Corregimos sobre el propio csv las estaciones de Guadalaja y Cordoba situadas en Mexico



# 3.- Configuracion API Google ------------------------------------
#------------------------------------------------------------------

# La clave se introduce para la ejecucion pero luego se omitira para no compartirla en el repo
API_key = 'AIzaSyDdOfLJPc0SZC0PoYzw4iukI6pnNv2L2_k'
gmaps = googlemaps.Client(key=API_key)



# 4.- Calculo Distancias -----------------------------------------
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


# Bucle que recorre cada par de filas y calcula la distancia
for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
    
    # Se asigna la latitud y longitud del punto de origen
    LatOrigin = row1['Latitude'] 
    LongOrigin = row1['Longitude']
    origins = (LatOrigin,LongOrigin)
    
    # Se asigna la latitud y longitud de la fila siguiente
    LatDest = row2['Latitude']
    LongDest = row2['Longitude']
    destination = (LatDest,LongDest)


    # Se llama a la funcion distance_matrix de google
      result = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
      

    # Se apendiza el resultado a la lista de distancias
      list.append(result)


# Se crea una columna con las distancias
df['Distance'] = list



# 6.- Output ------------------------------------------------------
#------------------------------------------------------------------

# df.to_csv('/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/ciudades_distancia.csv', sep = ";", index = False)


