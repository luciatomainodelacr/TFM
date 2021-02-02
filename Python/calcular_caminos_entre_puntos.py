#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# =============================================================================
#  CALCULA RUTA OPTIMA ENTRE DOS PUNTOS
# =============================================================================

"""
    Escenario de validacion:
    {
            "name": "Python: Camino entre 2 puntos",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "args": ["--tipo_programa","PUNTO_RECARGA","--marca_coche","VOLKSWAGEN","--modelo_coche","ID3 PURE",
                     "--origen","Alicante Tren","--destino","A Corunia Bus","--carga_inicial","65",
                     "--carga_final","70","--tipo_conector","IEC62196Type2Outlet"],
            "console": "integratedTerminal"
    }

    Ejecutar desde visual studio code: Debug

    Ejecutar en terminal
    >> cd /home/tfm/Documentos/TFM/Python/Modelo
    >> python3 calcular_caminos_entre_puntos.py --tipo_programa 'PUNTO_RECARGA' --marca_coche 'VOLKSWAGEN' --modelo_coche 'ID3 PURE' --origen 'Alicante Tren' --destino 'A Corunia Bus' --carga_inicial 65 --carga_final 70 --tipo_conector 'IEC62196Type2Outlet'

    Output esperado en log:
    [2021-01-31 21:25:19,833] [INFO    ]La ruta optima es: ['Alicante Tren', 'punto_recarga_241', 'punto_recarga_46', 'punto_recarga_262', 'punto_recarga_282', 'punto_recarga_293', 'A Corunia Bus']
    [2021-01-31 21:25:19,847] [INFO    ]Tiempo de parada en Alicante Tren es 0.0 h
    [2021-01-31 21:25:19,847] [INFO    ]Tiempo total del tramo Alicante Tren - punto_recarga_241 es 1.4135107859234253 h
    [2021-01-31 21:25:19,858] [INFO    ]Tiempo de parada en punto_recarga_241 es 0.27490825688073395 h
    [2021-01-31 21:25:19,858] [INFO    ]Tiempo total del tramo punto_recarga_241 - punto_recarga_46 es 1.9223443757129164 h
    [2021-01-31 21:25:19,869] [INFO    ]Tiempo de parada en punto_recarga_46 es 0.3856756756756757 h
    [2021-01-31 21:25:19,869] [INFO    ]Tiempo total del tramo punto_recarga_46 - punto_recarga_262 es 2.542525921501569 h
    [2021-01-31 21:25:19,880] [INFO    ]Tiempo de parada en punto_recarga_262 es 0.6113513513513513 h
    [2021-01-31 21:25:19,881] [INFO    ]Tiempo total del tramo punto_recarga_262 - punto_recarga_282 es 2.65368426054334 h
    [2021-01-31 21:25:19,892] [INFO    ]Tiempo de parada en punto_recarga_282 es 0.3856756756756757 h
    [2021-01-31 21:25:19,892] [INFO    ]Tiempo total del tramo punto_recarga_282 - punto_recarga_293 es 1.8773805206251493 h
    [2021-01-31 21:25:19,903] [INFO    ]Tiempo de parada en punto_recarga_293 es 0.8370270270270269 h
    [2021-01-31 21:25:19,904] [INFO    ]Tiempo total del tramo punto_recarga_293 - A Corunia Bus es 1.4841193792814318 h
    [2021-01-31 21:25:19,904] [INFO    ]El tiempo total tardado es: 11.89356524358783 h

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
os.chdir('/home/tfm/Documentos/TFM/Python/')
import Output.BaseDatos as BaseDatos
import Modelo.Restricciones as Restricciones
import Modelo.Tiempos as Tiempos
import Modelo.Network as Network


# 2.- Funcion main ------------------------------------------------
#------------------------------------------------------------------
def main(tipo_programa,
         marca_coche,
         modelo_coche,
         origen,
         destino,
         carga_inicial,
         carga_final,
         tipo_conector,
         log_level = "INFO",
         log_path = os.getcwd() + "/logs/"):

    if not os.path.exists(log_path):
            os.makedirs(log_path)

    logging.basicConfig(format = "[%(asctime)s] [%(levelname)-8s]"
                                 "%(message)s",
                        filename = (str(log_path) + "calcular_caminos_entre_puntos_" 
                                    + str(datetime.datetime.now().strftime("%04Y%02m%02d")
                                    + ".log")),
                        level = log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("[OK] Llamada al script calcular_caminos_entre_puntos.py [OK]")
    logger.info("El programa lanzado es: %s %s %s %s %s %s %s %s %s %s",
                 tipo_programa,
                 marca_coche,
                 modelo_coche,
                 origen,
                 destino,
                 carga_inicial,
                 carga_final,
                 tipo_conector,
                 log_level,
                 log_path)

    try:
        # 1.- Carga de inputs desde Base de Datos -------------------------
        #------------------------------------------------------------------
        logger.info("1.- Carga de inputs desde Base de Datos")
        bd = BaseDatos.BaseDatos(host="localhost",
                                 puerto=3306,            
                                 usuario="root",            
                                 password="root",        
                                 basedatos="tfm") 
        logger.info("Crear conexion a DB")
        con = bd.crear_conexion()

        # Query a PuntosCarga
        logger.info("Query a PuntosCarga")
        sql_query_pc = "SELECT * FROM PuntosCarga"
        columnas_pc = ["id","latitude","longitude","name","streetName","provincia","ccaa","postalCode","connectorType","ratedPowerKW","num_connectors","status"]
        df_puntoscarga = bd.ejecutar_queries_select(con = con,
                                                    sql_query = sql_query_pc,
                                                    columnas = columnas_pc)

        #Query a Ciudades
        logger.info("Query a Ciudades")
        sql_query_ciudades = "SELECT * FROM Ciudades"
        columnas_ciudades = ["id","PROVINCIA","ADDRESS","Latitude","Longitude","COORDENADAS","status"]
        df_ciudades = bd.ejecutar_queries_select(con = con,
                                                sql_query = sql_query_ciudades,
                                                columnas = columnas_ciudades)
        df_ciudades.set_index(["id"], inplace=True)
        df_ciudades.drop("status",axis="columns", inplace=True)

        #Query a ElectriCar
        logger.info("Query a ElectriCar")
        sql_query_coche = "SELECT * FROM ElectricCar WHERE BRAND = %s AND MODEL = %s"
        columnas_coche = ["BRAND","MODEL","RANGE_KM","EFFICIENCY_WHKM","FASTCHARGE_KMH","RAPIDCHARGE","PLUGTYPE", "BATTERY_CAPACITY"]
        argumentos_coche= (marca_coche, modelo_coche)
        df_electricar =  bd.ejecutar_queries_select(con = con,
                                                    sql_query = sql_query_coche,
                                                    columnas = columnas_coche,
                                                    argumentos = argumentos_coche)
        autonomia_coche = 0.9*float(df_electricar["RANGE_KM"]) 
        # TODO: llamar a la funcion de autonomia real del coche (que deberia ir en el modulo Tiempos.py)

        #Query a Matriz_distancia_haversine
        logger.info("Query a Matriz_distancia_haversine")
        #La restriccion de autonomia se aplica directamente en la llamada a la query
        if tipo_programa == "GASOLINERA":
            sql_query_distancia = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'gasolinera%' AND Destino LIKE 'gasolinera%') OR (Origen LIKE %s AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'gasolinera%' AND Destino LIKE %s));"
            columnas_distancia = ["Origen","Destino","Distance_km"]
            argumentos_distancia = (autonomia_coche,origen,destino)
            df_distancias =  bd.ejecutar_queries_select(con = con,
                                                        sql_query = sql_query_distancia,
                                                        columnas = columnas_distancia,
                                                        argumentos = argumentos_distancia)
        elif tipo_programa == "PUNTO_RECARGA":
            sql_query_distancia = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'punto_recarga%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'punto_recarga%') OR (Origen LIKE 'punto_recarga%' AND Destino LIKE %s));"
            columnas_distancia = ["Origen","Destino","Distance_km"]
            argumentos_distancia = (autonomia_coche,origen,destino)
            df_distancias =  bd.ejecutar_queries_select(con = con,
                                                        sql_query = sql_query_distancia,
                                                        columnas = columnas_distancia,
                                                        argumentos = argumentos_distancia)
        else:
            sql_query_distancia = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'gasolinera%' AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'punto_recarga%' AND  Destino LIKE 'gasolinera%') OR (Origen LIKE 'gasolinera%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE 'punto_recarga%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'punto_recarga%' AND Destino LIKE %s) OR (Origen LIKE 'gasolinera%' AND Destino LIKE %s));"
            columnas_distancia = ["Origen","Destino","Distance_km"]
            argumentos_distancia = (autonomia_coche,origen,origen,destino,destino)
            df_distancias =  bd.ejecutar_queries_select(con = con,
                                                        sql_query = sql_query_distancia,
                                                        columnas = columnas_distancia,
                                                        argumentos = argumentos_distancia)
        logger.info("Cerrar conexion con DB")
        con.close()
        # 2.- Aplicar las restricciones -----------------------------------
        #------------------------------------------------------------------
        logger.info("2.- Aplicar las restricciones")

        # a) Restriccion de tipo de conector
        logger.info("a) Restriccion de tipo de conector")
        puntoscarga_reduced = []
        for index, punto_carga in df_puntoscarga.iterrows():
            if tipo_conector in punto_carga["connectorType"]:
                puntoscarga_reduced.append(str(punto_carga["id"]))
        df_puntoscarga_reduced = df_puntoscarga[df_puntoscarga["id"].isin(puntoscarga_reduced)]
        df_distancias_pc = df_distancias[(df_distancias["Origen"].str.contains("punto_recarga"))|(df_distancias["Destino"].str.contains("punto_recarga"))]
        restriccion_tipo_conector = Restricciones.restriccion_tipo_conector(distancias = df_distancias_pc,
                                                                            puntoscarga_reduced = puntoscarga_reduced)
        # b) Restriccion de primera parada
        logger.info("b) Restriccion de primera parada")
        df_distancias_origen = df_distancias[df_distancias["Origen"]==origen]
        restricciones_prim_par = Restricciones.restriccion_primera_parada(distancias_origen = df_distancias_origen,
                                                                          carga_inicial = float(carga_inicial),
                                                                          autonomia_coche = autonomia_coche)
        # c) Restriccion de ultima parada
        logger.info("c) Restriccion de ultima parada")
        df_distancias_destino = df_distancias[df_distancias["Destino"]==destino]
        restricciones_ult_par = Restricciones.restriccion_ultima_parada(distancias_destino = df_distancias_destino,
                                                                        carga_final = float(carga_final),
                                                                        autonomia_coche = autonomia_coche)
        # Se genera el dataframe reducido que cumple con todas las restricciones
        logger.info("Se genera el dataframe reducido que cumple con todas las restricciones")
        df_distancias_merged_1 = pd.merge(df_distancias, restriccion_tipo_conector, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged_2 = pd.merge(df_distancias_merged_1, restricciones_prim_par, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged = pd.merge(df_distancias_merged_2, restricciones_ult_par, on=['Origen', 'Destino'], how='outer')
        #TODO: Hacer esto de manera limpia y no con esta guarreria :)
        df_distancias_merged = df_distancias_merged.fillna(True)
        df_distancias_reduced = df_distancias_merged[(df_distancias_merged["Restr_con"] == True)&
                                                     (df_distancias_merged["Restr_prim_par"] == True)&
                                                     (df_distancias_merged["Restr_ult_par"] == True)]

        logger.info("df_distancias %s", df_distancias.shape)
        logger.info("df_distancias_reduced %s", df_distancias_reduced.shape)

        # 3.- Calcular tiempos (de recorrido y parada) --------------------
        #------------------------------------------------------------------
        logger.info("3.- Calcular tiempos (de recorrido y parada)")

        #a) Tiempo de recorrido
        logger.info("a) Tiempo de recorrido")
        velocidad_coche = 100 #km/h
        df_distancias_reduced["Time_h"] = Tiempos.calcular_tiempo_recorrido(df_distancias_reduced["Distance_km"],velocidad_coche) #h

        #a) Tiempo de parada
        logger.info("b) Tiempo de parada")
        tiempos_puntos_parada = []

        if tipo_programa != "GASOLINERA":
            #Para los puntos de recarga, hay datos disponibles para el cálculo
            logger.info("Calculo tiempo de parada para puntos de recarga")
            capacidad_coche = float(df_electricar["BATTERY_CAPACITY"])*1000 #Wh
            df_puntoscarga_reduced[df_puntoscarga_reduced["ratedPowerKW"]== ''] = 10 #KW
            for index, punto_carga in df_puntoscarga_reduced.iterrows():
                numero_conectores_pc = int(punto_carga["num_connectors"])
                if numero_conectores_pc == 1:
                    potencia_pc = 0.9*float(punto_carga["ratedPowerKW"])*1000 #W
                else:
                    conectores = punto_carga["connectorType"].split(",")
                    conectores_limpio = []
                    for elem in conectores:
                        conectores_limpio.append(re.sub('[^A-Za-z0-9]+', '', elem))
                    indice = conectores_limpio.index(tipo_conector)
                    potencias = punto_carga["ratedPowerKW"].split(",")
                    potencias_limpio = []
                    for elem in potencias:
                        potencias_limpio.append(re.sub('[^A-Za-z0-9]+', '', elem))
                    potencia_pc = 0.9*float(potencias_limpio[indice])*1000 #W
                tiempos_puntos_parada.append((punto_carga["id"],Tiempos.calcular_tiempo_parada(capacidad_coche,potencia_pc,numero_conectores_pc)))

            column_names = ["id","Parada_h"]
            df_tiempos_puntos_parada = pd.DataFrame(data = tiempos_puntos_parada, columns = column_names)
        else:
            #TODO: Para los gasolineras, hay que ver como se calculan los datos (nos lo inventamos?)
            column_names = ["id","Parada_h"]
            df_tiempos_puntos_parada = pd.DataFrame(data = tiempos_puntos_parada, columns = column_names)

        # Se genera el dataframe reducido con columna basada en Suma_time_parada_h
        logger.info("Se genera el dataframe reducido con columna basada en Suma_time_parada_h")
        df_distancias_reduced = df_distancias_reduced.merge(df_tiempos_puntos_parada, how = "left", left_on = "Origen", right_on = "id")
        df_distancias_reduced["Parada_h"]           = df_distancias_reduced["Parada_h"].fillna(value = 0)
        df_distancias_reduced["Suma_time_parada_h"] = df_distancias_reduced["Time_h"] + df_distancias_reduced["Parada_h"]

        # Backup 
        df = df_distancias_reduced
        df

        # 4.- Construir el grafo ------------------------------------------
        #------------------------------------------------------------------

        logger.info("4.- Construir el grafo")
        DG = nx.DiGraph()
        for row in df.iterrows():
            DG.add_edge(row[1]["Origen"],
                        row[1]["Destino"],
                        time = row[1]["Suma_time_parada_h"])
        # Ver los nodos
        DG.nodes(data = True)

        # 5.- Calculo rutas optimas ---------------------------------------
        #------------------------------------------------------------------
        logger.info("5.- Calculo rutas optimas")
        """
        weight = None --> Busca el camino mas corto en numero de nodos
        weight = "distance" --> Busca el camino mas corto segun la distancia
        weight = "time" --> Busca el camino mas corto segun el tiempo
        """

        path = list(nx.astar_path(DG, source = origen, target = destino, weight = "time"))
        logger.info("La ruta optima es: %s", path)
        total_tiempo = 0
        for index, lugar  in enumerate(path):
            if index > 0:
                lugar_anterior = path[index-1]
                df_distancias_lugar = df_distancias_reduced[(df_distancias_reduced["Destino"]==lugar)&(df_distancias_reduced["Origen"]==lugar_anterior)]
                logger.info("Tiempo de parada en %s es %s h",lugar_anterior,float(df_distancias_lugar["Parada_h"]))
                logger.info("Tiempo total del tramo %s - %s es %s h",lugar_anterior,lugar,float(df_distancias_lugar["Suma_time_parada_h"]))
                total_tiempo = total_tiempo + float(df_distancias_lugar["Suma_time_parada_h"])
        logger.info("El tiempo total tardado es: %s h", total_tiempo)

        Network.get_shortest_path(DG, origen = origen, destino = destino)

        # 6.- Carga de outputs a Base de Datos ----------------------------
        #------------------------------------------------------------------
        logger.info("6.- Carga de outputs a Base de Datos")
        bd_output = BaseDatos.BaseDatos(host="localhost",
                                        puerto=3306,            
                                        usuario="root",            
                                        password="root",        
                                        basedatos="tfm") 
        logger.info("Crear conexion a DB")
        con = bd_output.crear_conexion()
        
        """# Query a PuntosCarga
        logger.info("Query a PuntosCarga")
        sql_query_pc = "SELECT * FROM PuntosCarga"
        columnas_pc = ["id","latitude","longitude","name","streetName","provincia","ccaa","postalCode","connectorType","ratedPowerKW","num_connectors","status"]
        df_puntoscarga = bd.ejecutar_queries_select(con = con,
                                                    sql_query = sql_query_pc,
                                                    columnas = columnas_pc)
        """
        logger.info("Cerrar conexion con DB")
        con.close()
        
        logger.info("[OK] Final del script calcular_caminos_entre_puntos.py [OK]")
        return True
    except:
        logger.error("El programa no ha podido obtener una ruta")
        return False

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
                        default = os.getcwd() + "/logs/",
                        type = str,
                        help = "Path del logging "
                               "Default: path actual")
    args = parser.parse_args()

    main(tipo_programa = args.tipo_programa,
         marca_coche = args.marca_coche,
         modelo_coche = args.modelo_coche,
         origen = args.origen,
         destino = args.destino,
         carga_inicial = args.carga_inicial,
         carga_final = args.carga_final,
         tipo_conector = args.tipo_conector,
         log_level = args.log_level,
         log_path = args.log_path)
    
