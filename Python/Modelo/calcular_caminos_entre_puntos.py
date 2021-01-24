# =============================================================================
#  CALCULA RUTA OPTIMA ENTRE DOS PUNTOS
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
    - Distancia: 157.112 kilometros
157.112
    Estacion de Autobuses de Soria -> Estacion de Autobuses de Zamora
    - Distancia: 303.507 kilometros
303.507

     Total Distancia: 460.619 km 
"""


# Se cargan las librerias
import networkx as nx
import os
import pandas as pd
import sys
import mysql.connector

import ModeloAvanzado.funcion_aux as fa

#FUNCIONES

# Funcion que devuelve la duracion completa del trayecto 
def show_path(path):
    try:
        total_distancia = 0

        for i in range(len(path)-1):
            origen = path[i]
            destino = path[i+1]
            distancia = DG[origen][destino]["distance"]

            total_distancia = total_distancia + distancia

            print("    %s -> %s\n    - Distancia: %s kilometros" % (
                df_ciudades.loc[origen]["ADDRESS"],
                df_ciudades.loc[destino]["ADDRESS"],
                distancia)
            )
            print(distancia)        
    
        print("\n     Total Distancia: %s km \n" % (total_distancia))
    except:
        print("No hay ruta válida para ", path)

# Funcion que calcule todos los caminos posible y muestre los que tienen menor distancia
def get_all_shortest_paths(DiGraph, origen, destino):
    try:
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
    except:
        print("No hay ruta válida desde ", origen," hasta ", destino)

# Camino mas corto
def get_shortest_path(DiGraph, origen, destino):
    try:
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
    except:
            print("No hay ruta válida desde ", origen," hasta ", destino)

#MAIN
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: This program needs at least 2 parameters: program_name program_type")
        sys.exit(1)
    else:
        print("The number of arguments is ", len(sys.argv))
        program_name = sys.argv[0]
        # program type can be: "ALL"
        program_type = sys.argv[1]
        print("The program run is: ",program_name, program_type)

    # 1.- Carga de inputs ---------------------------------------------
    #------------------------------------------------------------------
    #Crear conexión a la base de datos 
    con = mysql.connector.connect(host="localhost",
                                  port=3306,            
                                  user="root",            
                                  password="root",        
                                  database="tfm")
    
    cur = con.cursor()
    sql_query = "SELECT * FROM Ciudades_distancia"
    cur.execute(sql_query)
    df_distancias_db = pd.DataFrame(cur.fetchall(), columns = ["Origen","Destino","Distance_m"])
    sql_query = "SELECT * FROM Ciudades"
    cur.execute(sql_query)
    df_ciudades_db = pd.DataFrame(cur.fetchall(), columns = ["indice","CAPITAL DE PROVINCIA","ADDRESS","Latitude","Longitude","status"])

    con.close()

    df_ciudades_db.drop("indice",axis="columns", inplace=True)
    df_ciudades_db.drop("CAPITAL DE PROVINCIA",axis="columns", inplace=True)
    df_ciudades_db.drop("status",axis="columns", inplace=True)
    df_distancias_db["Distance_km"] = df_distancias_db["Distance_m"]/1000 # Pasar de m a km

    # Importar desde fichero 
    # Se establece el diretorio base
    os.chdir('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI')
    df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'ciudades.csv'), sep = ',', encoding = 'iso-8859-1', decimal = '.')
    df_ciudades.set_index(["CAPITAL DE PROVINCIA"], inplace=True)
    df_ciudades.drop("COORDENADAS",axis="columns", inplace=True)

    df_distancias = pd.read_csv(os.path.join(os.getcwd(),'ciudades_distancia.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')

    # La columna de km no está bien del todo. La borramos y la generamos en funcion de la que está en metros (Distance_m)
    df_distancias.drop("Distance_km",axis="columns", inplace=True)
    df_distancias["Distance_km"] = df_distancias["Distance_m"]/1000 # Pasar de m a km
    
    print(df_distancias_db.equals(df_ciudades))
    print(df_ciudades_db.equals(df_distancias))

    # Filtrar el df_distancias con las restricciones del Modelo Avanzado
    # a) Restricción de autonomía
    autonomia_coche = 200 #km
    restricciones_autonomia = fa.restriccion_autonomia(df_distancias["Distance_km"],autonomia_coche)
    df_distancias_merged = pd.merge(df_distancias, restricciones_autonomia, left_index=True, right_index=True)
    # b) Otras restricciones
    # Se genera el dataframe reducido que cumple con todas las restricciones
    df_distancias_reduced = df_distancias_merged[df_distancias_merged["Restr_aut"] == True]

    print("df_distancias", df_distancias.shape)
    print("df_distancias_reduced", df_distancias_reduced.shape)
    # Backup 
    df = df_distancias_reduced
    df

    # 2.- Grafo -------------------------------------------------------
    #------------------------------------------------------------------

    # Construir el grafo
    DG = nx.DiGraph()

    for row in df.iterrows():
        DG.add_edge(row[1]["Origen"],
                    row[1]["Destino"],
                    distance = row[1]["Distance_km"])

    # Ver los nodos
    DG.nodes(data = True)

    # 3.- Calculo rutas optimas ---------------------------------------
    #------------------------------------------------------------------

    """
    weight = None --> Busca el camino mas corto en nº de nodos
    weight = "distance" --> Busca el camino mas corto segun la distancia
    """

    # Encuentra todas las rutas entre dos puntos
    #list(nx.all_shortest_paths(DG, source = "Zaragoza Tren", target = "Zamora Bus", weight = None))

    # Dijkstra - Encuentra la ruta con menor distancia
    #list(nx.dijkstra_path(DG, source = "Zaragoza Tren", target = "Zamora Bus", weight = "distance"))

    # A* - Encuentra la ruta con menor distancia (Mas optimo que Dijstra)
    #list(nx.astar_path(DG, ("Zaragoza Tren"), ("Zamora Bus"), weight = "distance"))

    # Se pasa como argumento la ruta obtenida
    #show_path(['Zaragoza Tren', 'Soria Bus', 'Zamora Bus'])
    #get_all_shortest_paths(DG, 'Zaragoza Tren', 'Zamora Bus')

    # Ejemplos
    get_shortest_path(DG, origen = "Zaragoza Tren", destino = "Zamora Bus")
    #get_all_shortest_paths(DG, origen = "Alicante Tren", destino = "A Corunia Bus")
    get_shortest_path(DG, origen = "Alicante Tren", destino = "A Corunia Bus")

