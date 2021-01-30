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

Ejecutar desde el terminal: python3 calcular_caminos_entre_puntos.py DB VOLKSWAGEN "ID3 PURE" "Alicante Tren" "A Corunia Bus" 65 70

"""


# Se cargan las librerias
import networkx as nx
import os
import pandas as pd
import sys
import mysql.connector


# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Python/Modelo/')


import ModeloAvanzado.funcion_aux as fa



# 1.- Se definen las funciones ------------------------------------
#------------------------------------------------------------------

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


# 2.- Main --------------------------------------------------------
#------------------------------------------------------------------

if __name__ == "__main__":
    
    if len(sys.argv) != 8:
        print("""ERROR: Este programa necesita 8 parametros: nombre_programa
            tipo_programa marca_coche modelo_coche origen destino carga_inicial 
            carga_final""")
        sys.exit(1)
    else:
        print("The number of arguments is ", len(sys.argv))
        program_name = sys.argv[0]
        # program type can be: "DB, CSV"
        program_type = sys.argv[1]
        car_brand = sys.argv[2]
        car_model = sys.argv[3]
        origin = sys.argv[4]
        destination = sys.argv[5]
        initial_charge = float(sys.argv[6])
        final_charge = float(sys.argv[7])
        print("El programa lanzado es: ",program_name, program_type,
        car_brand, car_model, origin, destination, initial_charge, final_charge)

    try:

        # 1.- Carga de inputs ---------------------------------------------
        #------------------------------------------------------------------

        if program_type == "DB":

            # Crear conexión a la base de datos 
            con = mysql.connector.connect(host="localhost",
                                        port=3306,            
                                        user="root",            
                                        password="root",        
                                        database="tfm")

            cur = con.cursor()
            sql_query = "SELECT * FROM Ciudades_distancia"
            cur.execute(sql_query)
            df_distancias = pd.DataFrame(cur.fetchall(), columns = ["Origen","Destino","Distance_m"])

            sql_query = "SELECT * FROM Ciudades"
            cur.execute(sql_query)
            df_ciudades = pd.DataFrame(cur.fetchall(), columns = ["indice","CAPITAL DE PROVINCIA","ADDRESS","Latitude","Longitude","status"])

            sql_query = "SELECT * FROM ElectricCar WHERE BRAND = %s AND MODEL = %s"
            arg = (car_brand,car_model)
            cur.execute(sql_query, arg)
            df_electricar = pd.DataFrame(cur.fetchall(), columns = ["BRAND","MODEL","RANGE_KM","EFFICIENCY_WHKM","FASTCHARGE_KMH","RAPIDCHARGE","PLUGTYPE", "BATTERY_CAPACITY"])

            # sql_query = "SELECT * FROM PuntosCarga"
            # cur.execute(sql_query, arg)
            # df_puntoscarga = pd.DataFrame(cur.fetchall(), columns = ["indice","name","formatted_address","latitude","longitude","province","status"])

            con.close()

            df_ciudades.set_index(["CAPITAL DE PROVINCIA"], inplace=True)
            df_ciudades.drop("indice",axis="columns", inplace=True)
            df_ciudades.drop("status",axis="columns", inplace=True)

            df_distancias["Distance_km"] = df_distancias["Distance_m"]/1000 # Pasar de m a km

        elif program_type == "CSV":
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

            df_electricar = pd.read_csv('/home/tfm/Documentos/TFM/Datasets/CochesElectricos/coches electricos/electricCar_limpio.csv', sep = ',', encoding = 'iso-8859-1', decimal = '.')
            df_electricar = df_electricar[(df_electricar["BRAND"]==car_brand)&(df_electricar["MODEL"]==car_model)]

        # Filtrar el df_distancias con las restricciones del Modelo Avanzado

        # a) Restricción de autonomía
        autonomia_coche = int(df_electricar["RANGE_KM"]) #km
        restricciones_autonomia = fa.restriccion_autonomia(df_distancias,autonomia_coche)
        # b) Restricción de primera parada
        df_distancias_origen = df_distancias[df_distancias["Origen"]==origin]
        restricciones_prim_par = fa.restriccion_primera_parada(df_distancias_origen,initial_charge,autonomia_coche)
        # c) Restricción de última parada
        df_distancias_destino = df_distancias[df_distancias["Destino"]==destination]
        restricciones_ult_par = fa.restriccion_ultima_parada(df_distancias_destino,final_charge,autonomia_coche)
        # Se genera el dataframe reducido que cumple con todas las restricciones
        df_distancias_merged_1 = pd.merge(df_distancias, restricciones_autonomia, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged_2 = pd.merge(df_distancias_merged_1, restricciones_prim_par, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged = pd.merge(df_distancias_merged_2, restricciones_ult_par, on=['Origen', 'Destino'], how='outer')
        #TODO: Hacer esto de manera limpia y no con esta guarreria :)
        df_distancias_merged = df_distancias_merged.fillna(True)
        df_distancias_reduced = df_distancias_merged[(df_distancias_merged["Restr_aut"] == True)&(df_distancias_merged["Restr_prim_par"] == True)&
                                                     (df_distancias_merged["Restr_ult_par"] == True)]

        print("df_distancias", df_distancias.shape)
        print("df_distancias_reduced", df_distancias_reduced.shape)

        # Calcular funcion objetivo
        # velocidad = 100 #km/h
        # for index, puntos_carga in df_puntoscarga.iterrows():
        #     numero_conectores_pc = 1
        #     carga = 1
        #     df_distancias_reduced_or = df_distancias_reduced[df_distancias_reduced["Origen"]==puntos_carga["name"]]
        #     df_distancias_reduced_dest = df_distancias_reduced[df_distancias_reduced["Destino"]==puntos_carga["name"]]
        #     df_distancias_puntos_carga = pd.concat([df_distancias_reduced_or,df_distancias_reduced_dest])
        #     for index, distancia_puntos_carga in df_distancias_puntos_carga.iterrows():
        #         df_tiempos[puntos_carga["name"]] = fa.funcion_objetivo_tiempo(distancia_puntos_carga["Distance_km"],velocidad,carga,numero_conectores_pc)
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
        #get_shortest_path(DG, origen = "Zaragoza Tren", destino = "Zamora Bus")
        #get_all_shortest_paths(DG, origen = "Alicante Tren", destino = "A Corunia Bus")
        get_shortest_path(DG, origen = origin, destino = destination)
    except:
        print("El programa no ha podido obtener una ruta")

