# =============================================================================
#  MODELO DE OPTIMIZACION - CALCULA RUTA ENTRE DOS PUNTOS
# =============================================================================

"""
Fuente: http://sukiweb.net/archivos/2018/05/30/encontrando-caminos-optimos-con-grafos-en-python/

Input: lista de ciudades, matriz de distancias entre las ciudades

Proceso: Dadas dos ciudades origen-destino calcula la ruta optima entre ellas,
o bien por el numero de nodos minimos necesarios para llegar o bien por el 
target que se le indique, en este caso, minimizar la distancia total.

Output: Ruta optima entre el origen y destino

Ej:
>> get_all_shortest_paths(DG, 'Zaragoza Tren', 'Zamora Bus')

Camino óptimo: ['Zaragoza Tren', 'Soria Bus', 'Zamora Bus']
    Estacion de Zaragoza -> Estacion de Autobuses de Soria
    - Distancia: 157112 metros
157112
    Estacion de Autobuses de Soria -> Estacion de Autobuses de Zamora
    - Distancia: 303507 metros
303507

     Total Distancia: 460619 m 
"""


# Se cargan las librerias
import networkx as nx
import os
import pandas as pd

# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI')



# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'ciudades.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')
df_ciudades.set_index(["CAPITAL DE PROVINCIA"], inplace=True)


df_distancias = pd.read_csv(os.path.join(os.getcwd(),'ciudades_distancia.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')

# Backup 
df = df_distancias
df



# 2.- Grafo -------------------------------------------------------
#------------------------------------------------------------------

# Construir el grafo
DG = nx.DiGraph()

for row in df.iterrows():
    DG.add_edge(row[1]["Origen"],
                row[1]["Destino"],
                distance = row[1]["Distance_m"])

# Ver los nodos
DG.nodes(data = True)



# 2.- Calculo rutas optimas ---------------------------------------
#------------------------------------------------------------------

"""
weight = None --> Busca el camino mas corto en nº de nodos
weight = "distance" --> Busca el camino mas corto segun la distancia
"""

# Encuentra todas las rutas entre dos puntos
list(nx.all_shortest_paths(DG, source = "Zaragoza Tren", target = "Zamora Bus", weight = None))

# Dijkstra - Encuentra la ruta con menor distancia
list(nx.dijkstra_path(DG, source = "Zaragoza Tren", target = "Zamora Bus", weight = "distance"))

# A* - Encuentra la ruta con menor distancia (Mas optimo que Dijstra)
list(nx.astar_path(DG, ("Zaragoza Tren"), ("Zamora Bus"), weight = "distance"))


# Funcion que devuelve la duracion completa del trayecto 
def show_path(path):
    total_distancia = 0
    
    for i in range(len(path)-1):
        origen = path[i]
        destino = path[i+1]
        distancia = DG[origen][destino]["distance"]
                
        total_distancia = total_distancia + distancia

        print("    %s -> %s\n    - Distancia: %s metros" % (
            df_ciudades.loc[origen]["ADDRESS"],
            df_ciudades.loc[destino]["ADDRESS"],
            distancia)
        )
        
        print(distancia)        
    
    print("\n     Total Distancia: %s m \n" % (total_distancia))


# Se pasa como argumento la ruta obtenida
show_path(['Zaragoza Tren', 'Soria Bus', 'Zamora Bus'])


# Funcion que calcule todos los caminos posible y muestre los que tienen menor distancia
def get_all_shortest_paths(DiGraph, origen, destino):
    print("*** All shortest paths - Origen: %s Destino: %s" % (
        origen, destino
    ))
    for weight in [None, "distance"]:
        print("* Ordenando por: %s" % weight)
        paths = list(nx.all_shortest_paths(DiGraph,
                                          source = origen,
                                          target = destino,
                                          weight = weight))
        for path in paths:
            print("   Camino óptimo: %s" % path)
            show_path(path)


get_all_shortest_paths(DG, 'Zaragoza Tren', 'Zamora Bus')



# Camino mas corto
def get_shortest_path(DiGraph, origen, destino):
    print("*** Origen: %s Destino: %s" % (origen, destino))
    
    for weight in ["distancia"]:
        print(" Ordenado por: %s" % weight)
        path = list(nx.astar_path(DiGraph,
                                  (origen),
                                  (destino),
                                  weight = weight
                                 ))

        print("   Camino óptimo: %s " % path)
        show_path(path)


# Ejemplos
get_shortest_path(DG, origen = "Zaragoza Tren", destino = "Zamora Bus")
get_all_shortest_paths(DG, origen = "Alicante Tren", destino = "A Corunia Bus")


