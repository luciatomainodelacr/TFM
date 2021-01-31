#!/usr/bin/python3.6
# =============================================================================
#  CALCULA RUTA OPTIMA ENTRE DOS PUNTOS
# =============================================================================

"""
    Escenario de validacióon:
    {
            "name": "Python: Camino entre 2 puntos",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "args": ["PUNTO_RECARGA","VOLKSWAGEN","ID3 PURE","Alicante Tren","A Corunia Bus", "65", "70","IEC62196Type2Outlet"],
            "console": "integratedTerminal"
    }

    Ejecutar desde visual studio code: Debug

    Ejecutar en terminal
    >> cd /Python/Modelo
    >> python3 calcular_caminos_entre_puntos.py PUNTO_RECARGA VOLKSWAGEN "ID3 PURE" "Alicante Tren" "A Corunia Bus" 65 70 IEC62196Type2Outlet

"""


# 1.- Se cargan las librerias -------------------------------------
#------------------------------------------------------------------

import os, sys
import networkx as nx
import pandas as pd
import mysql.connector
import re
import argparse
import logging
import datetime

# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Python/Modelo/')
import BaseDatos
import Restricciones
import funcion_aux as fa 


# 2.- Funcion main ------------------------------------------------
#------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcular caminos entre puntos")
    parser.add_argument("--tipo_programa",
                        required = False,
                        type = str,
                        choices = ["GASOLINERA","PUNTO_RECARGA","ALL"],
                        default = "ALL",
                        help = "Tipo de programa en base a los puntos que se quieren usar "
                               "Default: ALL")
    parser.add_argument("--marca_coche",
                        required = True,
                        type = str,
                        help = "Marca de coche (tiene que estar en la tabla ElectricCar)")
    parser.add_argument("--modelo_coche",
                        required = True,
                        type = str,
                        help = "Modelo de coche (tiene que estar en la tabla ElectricCar)")
    parser.add_argument("--origen",
                        required = True,
                        type = str,
                        help = "Lugar de Origen (tiene que estar en la tabla Ciudades)")
    parser.add_argument("--destino",
                        required = True,
                        type = str,
                        help = "Lugar de Destino (tiene que estar en la tabla Ciudades)")
    parser.add_argument("--carga_inicial",
                        required = False,
                        type = str,
                        default = "90",
                        help = "Porcentaje de carga inicial del coche en lugar de origen "
                               "Default: 90")
    parser.add_argument("--carga_final",
                        required = False,
                        type = str,
                        default = "10",
                        help = "Porcentaje de carga final del coche en lugar de destino "
                               "Default: 10")
    parser.add_argument("--tipo_conector",
                        required = True,
                        type = str,
                        help = "Tipo de conector que necesita el coche (tiene que estar en la tabla PuntosCarga)")
    parser.add_argument("--log_level",
                        required = False,
                        default = "INFO",
                        choices = ["DEBUG","INFO","WARNING","ERROR"],
                        help = "Nivel de logging "
                               "Default: INFO")
    parser.add_argument("--log_path",
                        required = False,
                        type = str,
                        help = "Path del logging "
                               "Default: path actual")
    args = parser.parse_args()

    if args.log_path:
        log_path = args.log_path
        # Si el log_path no existe, se crea
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    else:
        log_path = os.getcwd() + "/"
    
    logging.basicConfig(format = "[%(asctime)s] [%(levelname)-8s]"
                                 "%(message)s",
                        filename = (str(log_path) + "calcular_caminos_entre_puntos_" 
                                    + str(datetime.datetime.now().strftime("%04Y%02m%02d")
                                    + ".log")),
                        level = args.log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("[OK] Llamada al script calcular_caminos_entre_puntos.py [OK]")
    logger.info("El programa lanzado es: ",
                 args.tipo_programa, " ",
                 args.marca_coche, " ",
                 args.modelo_coche, " ",
                 args.origen, " ",
                 args.destino, " ",
                 args.carga_inicial, " ",
                 args.carga_final, " ",
                 args.tipo_conector)

    try:

        # 1.- Carga de inputs desde Base de Datos -------------------------
        #------------------------------------------------------------------
        
        bd = BaseDatos.BaseDatos(host="localhost",
                                 puerto=3306,            
                                 usuario="root",            
                                 password="root",        
                                 basedatos="tfm") 
        con = bd.crear_conexion()

        # Query a PuntosCarga
        sql_query_pc = "SELECT * FROM PuntosCarga"
        columnas_pc = ["id","latitude","longitude","name","streetName","provincia","ccaa","postalCode","connectorType","ratedPowerKW","num_connectors","status"]
        df_puntoscarga = bd.ejecutar_queries(con = con,
                                             sql_query = sql_query_pc,
                                             columnas = columnas_pc)

        #Query a Ciudades
        sql_query_ciudades = "SELECT * FROM Ciudades"
        columnas_ciudades = ["id","PROVINCIA","ADDRESS","Latitude","Longitude","COORDENADAS","status"]
        df_ciudades = bd.ejecutar_queries(con = con,
                                          sql_query = sql_query_ciudades,
                                          columnas = columnas_ciudades)

        df_ciudades.set_index(["id"], inplace=True)
        df_ciudades.drop("status",axis="columns", inplace=True)

        #Query a ElectriCar
        sql_query_coche = "SELECT * FROM ElectricCar WHERE BRAND = %s AND MODEL = %s"
        columnas_coche = ["BRAND","MODEL","RANGE_KM","EFFICIENCY_WHKM","FASTCHARGE_KMH","RAPIDCHARGE","PLUGTYPE", "BATTERY_CAPACITY"]
        argumentos_coche= (args.marca_coche, args.modelo_coche)
        df_electricar =  bd.ejecutar_queries(con = con,
                                             sql_query = sql_query_coche,
                                             columnas = columnas_coche,
                                             argumentos = argumentos_coche)
        autonomia_coche = 0.9*float(df_electricar["RANGE_KM"]) # TODO: llamar a la funcion de autonomia real del coche

        #La restriccion de autonomia se aplica directamente en la llamada a la query
        if args.tipo_programa == "GASOLINERA":
            sql_query_distancia = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'gasolinera%' AND Destino LIKE 'gasolinera%') OR (Origen LIKE %s AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'gasolinera%' AND Destino LIKE %s));"
            columnas_distancia = ["Origen","Destino","Distance_km"]
            argumentos_distancia = (autonomia_coche,args.origen,args.destino)
            df_distancias =  bd.ejecutar_queries(con = con,
                                                 sql_query = sql_query_distancia,
                                                 columnas = columnas_distancia,
                                                 argumentos = argumentos_distancia)
        elif args.tipo_programa == "PUNTO_RECARGA":
            sql_query_distancia = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'punto_recarga%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'punto_recarga%') OR (Origen LIKE 'punto_recarga%' AND Destino LIKE %s));"
            columnas_distancia = ["Origen","Destino","Distance_km"]
            argumentos_distancia = (autonomia_coche,args.origen,args.destino)
            df_distancias =  bd.ejecutar_queries(con = con,
                                                 sql_query = sql_query_distancia,
                                                 columnas = columnas_distancia,
                                                 argumentos = argumentos_distancia)
        else:
            sql_query_distancia = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'gasolinera%' AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'punto_recarga%' AND  Destino LIKE 'gasolinera%') OR (Origen LIKE 'gasolinera%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE 'punto_recarga%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'punto_recarga%' AND Destino LIKE %s) OR (Origen LIKE 'gasolinera%' AND Destino LIKE %s));"
            columnas_distancia = ["Origen","Destino","Distance_km"]
            argumentos_distancia = (autonomia_coche,args.origen,args.origen,args.destino,args.destino)
            df_distancias =  bd.ejecutar_queries(con = con,
                                                 sql_query = sql_query_distancia,
                                                 columnas = columnas_distancia,
                                                 argumentos = argumentos_distancia)
        con.close()

        # 2.- Aplicar las restricciones -----------------------------------
        #------------------------------------------------------------------

        restriccion = Restricciones.Restricciones()
        # a) Restriccion de tipo de conector
        puntoscarga_reduced = []
        for index, punto_carga in df_puntoscarga.iterrows():
            if args.tipo_conector in punto_carga["connectorType"]:
                puntoscarga_reduced.append(str(punto_carga["id"]))
        df_puntoscarga_reduced = df_puntoscarga[df_puntoscarga["id"].isin(puntoscarga_reduced)]

        df_distancias_pc = df_distancias[(df_distancias["Origen"].str.contains("punto_recarga"))|(df_distancias["Destino"].str.contains("punto_recarga"))]
        restriccion.restriccion_tipo_conector(distancias = df_distancias_pc,
                                              puntoscarga_reduced = puntoscarga_reduced)

        # b) Restriccion de primera parada
        df_distancias_origen = df_distancias[df_distancias["Origen"]==args.origen]
        restriccion.restriccion_primera_parada(df_distancias_origen,float(args.carga_inicial),autonomia_coche)

        # c) Restriccion de ultima parada
        df_distancias_destino = df_distancias[df_distancias["Destino"]==args.destino]
        restriccion.restriccion_ultima_parada(df_distancias_destino,float(args.carga_final),autonomia_coche)

        # Se genera el dataframe reducido que cumple con todas las restricciones
        df_distancias_merged_1 = pd.merge(df_distancias, restriccion.restriccion_tipo_conector, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged_2 = pd.merge(df_distancias_merged_1, restriccion.restricciones_prim_par, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged = pd.merge(df_distancias_merged_2, restriccion.restricciones_ult_par, on=['Origen', 'Destino'], how='outer')
        #TODO: Hacer esto de manera limpia y no con esta guarreria :)
        df_distancias_merged = df_distancias_merged.fillna(True)
        df_distancias_reduced = df_distancias_merged[(df_distancias_merged["Restr_con"] == True)&
                                                     (df_distancias_merged["Restr_prim_par"] == True)&
                                                     (df_distancias_merged["Restr_ult_par"] == True)]

        print("df_distancias", df_distancias.shape)
        print("df_distancias_reduced", df_distancias_reduced.shape)

        # Calcular tiempo de recorrido y tiempo de parada
        velocidad_coche = 100 #km/h
        capacidad_coche = float(df_electricar["BATTERY_CAPACITY"])*1000 #Wh
        df_distancias_reduced["Time_h"] = fa.calcular_tiempo_recorrido(df_distancias_reduced["Distance_km"],velocidad_coche) #h
        df_puntoscarga_reduced[df_puntoscarga_reduced["ratedPowerKW"]== ''] = 10 #KW

        tiempos_puntos_parada = []
        for index, punto_carga in df_puntoscarga_reduced.iterrows():
            numero_conectores_pc = int(punto_carga["num_connectors"])
            if numero_conectores_pc == 1:
                potencia_pc = 0.9*float(punto_carga["ratedPowerKW"])*1000 #W
            else:
                conectores = punto_carga["connectorType"].split(",")
                conectores_limpio = []
                for elem in conectores:
                    conectores_limpio.append(re.sub('[^A-Za-z0-9]+', '', elem))
                indice = conectores_limpio.index(connector_type)
                potencias = punto_carga["ratedPowerKW"].split(",")
                potencias_limpio = []
                for elem in potencias:
                    potencias_limpio.append(re.sub('[^A-Za-z0-9]+', '', elem))
                potencia_pc = 0.9*float(potencias_limpio[indice])*1000 #W
            tiempos_puntos_parada.append((punto_carga["id"],fa.calcular_tiempo_parada(capacidad_coche,potencia_pc,numero_conectores_pc)))
        
        column_names = ["id","Parada_h"]
        df_tiempos_puntos_parada = pd.DataFrame(data = tiempos_puntos_parada, columns = column_names)

        df_distancias_reduced = df_distancias_reduced.merge(df_tiempos_puntos_parada, how = "left", left_on = "Origen", right_on = "id")

        df_distancias_reduced["Parada_h"]           = df_distancias_reduced["Parada_h"].fillna(value = 0)
        df_distancias_reduced["Suma_time_parada_h"] = df_distancias_reduced["Time_h"] + df_distancias_reduced["Parada_h"]


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
                        time = row[1]["Suma_time_parada_h"])

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

        fa.get_shortest_path(DG, origen = origin, destino = destination)
    except:
        print("El programa no ha podido obtener una ruta")

