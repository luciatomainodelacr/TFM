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
                     "--carga_final","70","--tipo_conector","IEC62196Type2Outlet","--user_id","2"],
            "console": "integratedTerminal"
    }

    Ejecutar desde visual studio code: Debug

    Ejecutar en terminal
    >> cd /home/tfm/Documentos/TFM/Python/Modelo
    >> python3 calcular_caminos_entre_puntos.py --tipo_programa 'PUNTO_RECARGA' --marca_coche 'VOLKSWAGEN' --modelo_coche 'ID3 PURE' --origen 'Alicante Tren' --destino 'A Corunia Bus' --carga_inicial 65 --carga_final 70 --tipo_conector 'IEC62196Type2Outlet'

    Output esperado en log:
[2021-02-04 22:43:03,447] [INFO    ]La ruta optima es: ['Alicante Tren', 'punto_recarga_241', 'punto_recarga_246', 'punto_recarga_263', 'punto
[2021-02-04 22:43:03,460] [INFO    ]Tiempo de parada en Alicante Tren es 0.0 h
[2021-02-04 22:43:03,461] [INFO    ]Tiempo total del tramo Alicante Tren - punto_recarga_241 es 1.4135107859234253 h
[2021-02-04 22:43:03,471] [INFO    ]Tiempo de parada en punto_recarga_241 es 1.3090825688073393 h
[2021-02-04 22:43:03,472] [INFO    ]Tiempo total del tramo punto_recarga_241 - punto_recarga_246 es 3.092301726368534 h
[2021-02-04 22:43:03,482] [INFO    ]Tiempo de parada en punto_recarga_246 es 2.4167567567567567 h
[2021-02-04 22:43:03,483] [INFO    ]Tiempo total del tramo punto_recarga_246 - punto_recarga_263 es 4.363408303110635 h
[2021-02-04 22:43:03,494] [INFO    ]Tiempo de parada en punto_recarga_263 es 2.4167567567567567 h
[2021-02-04 22:43:03,494] [INFO    ]Tiempo total del tramo punto_recarga_263 - punto_recarga_278 es 4.50142223671517 h
[2021-02-04 22:43:03,506] [INFO    ]Tiempo de parada en punto_recarga_278 es 2.4167567567567567 h
[2021-02-04 22:43:03,507] [INFO    ]Tiempo total del tramo punto_recarga_278 - punto_recarga_286 es 3.980899331229511 h
[2021-02-04 22:43:03,518] [INFO    ]Tiempo de parada en punto_recarga_286 es 2.4167567567567567 h
[2021-02-04 22:43:03,518] [INFO    ]Tiempo total del tramo punto_recarga_286 - A Corunia Bus es 2.4337595723944427 h
[2021-02-04 22:43:03,519] [INFO    ]El tiempo total tardado es: 19.78530195574172 h

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
import numpy as np

# Se establece el diretorio base
print(os.getcwd())
if __package__ is None or __package__ == '':
    # uses current directory visibility
    import Output.BaseDatos as BaseDatos
    import Modelo.Restricciones as Restricciones
    import Modelo.Tiempos as Tiempos
    import Modelo.Network as Network
else:
    # uses current package visibility
    from .Output import BaseDatos as BaseDatos
    from .Modelo import Restricciones as Restricciones
    from .Modelo import Tiempos as Tiempos
    from .Modelo import Network as Network


# 2.- Funcion main ------------------------------------------------
#------------------------------------------------------------------
def main_route(tipo_programa,
               marca_coche,
               modelo_coche,
               origen,
               destino,
               carga_inicial = "90",
               carga_final = "10",
               tipo_conector = "",
               log_level = "INFO",
               log_path = os.getcwd() + "/logs/",
               user_id = 1,
               use_docker = False):

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
        #------------------------------------------------------------------
        # 1.- Carga de inputs desde Base de Datos -------------------------
        logger.info("1.- Carga de inputs desde Base de Datos")
        if use_docker:
            db_host = "db"
        else:
            db_host = "localhost"
        bd = BaseDatos.BaseDatos(host=db_host,
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
        #Query a Gasolineras
        logger.info("Query a GasolinerasPropuesta")
        sql_query_gasolineras = "SELECT * FROM GasolinerasPropuesta"
        columnas_gasolineras = ["id","provincia","municipio","localidad","codigo_po","direccion","margen","longitud","latitud","rotulo","tipo_venta","rem_","horario","status"]
        df_gasolineras = bd.ejecutar_queries_select(con = con,
                                                    sql_query = sql_query_gasolineras,
                                                    columnas = columnas_gasolineras)
        #Query a Ciudades
        logger.info("Query a Ciudades")
        sql_query_ciudades = "SELECT * FROM Ciudades"
        columnas_ciudades = ["id","PROVINCIA","ADDRESS","Latitude","Longitude","COORDENADAS","status"]
        df_ciudades = bd.ejecutar_queries_select(con = con,
                                                 sql_query = sql_query_ciudades,
                                                 columnas = columnas_ciudades)
        #df_ciudades.set_index(["id"], inplace=True)
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
        logger.info("Query a Matriz_distancia_haversine completo")
        sql_query_distancia_completo = "SELECT * FROM Matriz_distancia_haversine"
        columnas_distancia_completo = ["Origen","Destino","Distance_km"]
        df_distancias_completo =  bd.ejecutar_queries_select(con = con,
                                                             sql_query = sql_query_distancia_completo,
                                                             columnas = columnas_distancia_completo)
        logger.info("Cerrar conexion con DB")
        con.close()
        # 2.- Aplicar las restricciones -----------------------------------
        #------------------------------------------------------------------
        logger.info("2.- Aplicar las restricciones")
        if tipo_conector != "":
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
        else:
            # a) Si no se especifica tipo de conector, no se aplica restriccion
            logger.info("a) Si no se especifica tipo de conector, no se aplica restriccion")
            df_puntoscarga_reduced = df_puntoscarga
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
        if tipo_conector != "":
            df_distancias_merged_1 = pd.merge(df_distancias, restriccion_tipo_conector, on=['Origen', 'Destino'], how='outer')
        else:
            df_distancias_merged_1 = df_distancias
        df_distancias_merged_2 = pd.merge(df_distancias_merged_1, restricciones_prim_par, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged = pd.merge(df_distancias_merged_2, restricciones_ult_par, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged = df_distancias_merged.fillna(True)
        if tipo_conector != "":
            df_distancias_reduced = df_distancias_merged[(df_distancias_merged["Restr_con"] == True)&
                                                        (df_distancias_merged["Restr_prim_par"] == True)&
                                                        (df_distancias_merged["Restr_ult_par"] == True)]
        else: 
            df_distancias_reduced = df_distancias_merged[(df_distancias_merged["Restr_prim_par"] == True)&
                                                        (df_distancias_merged["Restr_ult_par"] == True)]
        logger.info("df_distancias %s", df_distancias.shape)
        logger.info("df_distancias_reduced %s", df_distancias_reduced.shape)
        # 3.- Calcular tiempos (de recorrido y parada) --------------------
        #------------------------------------------------------------------
        logger.info("3.- Calcular tiempos (de recorrido y parada)")
        #a) Tiempo de recorrido
        logger.info("a) Tiempo de recorrido")
        velocidad_coche = 110 #km/h
        df_distancias_reduced["Time_h"] = Tiempos.calcular_tiempo_recorrido(df_distancias_reduced["Distance_km"],velocidad_coche) #h
        #b) Tiempo de parada
        logger.info("b) Tiempo de parada")
        # Filtro las distancias menores o iguales de 50 km entre las CIUDADES IMPORTANTES y 
        # el resto de coordenadas
        logger.info("Filtro las distancias menores o iguales de 50 km entre las CIUDADES IMPORTANTES y el resto de coordenadas")
        lista_ciudades_importantes = ["Madrid Tren", "Barcelona Tren", "Bilbao Tren", "Sevilla Tren", "Valencia Tren"]
        puntos_50km_ciud = []
        for ciudad in lista_ciudades_importantes:
            df1 = df_distancias_completo[df_distancias_completo["Origen"].str.contains(ciudad)]
            df1_50 = df1[df1['Distance_km']<= 50]
            for i in df1_50["Destino"]:
                puntos_50km_ciud.append(i)
            lista_definitiva = []
            for elemento in puntos_50km_ciud:
                if elemento[0:3] in ('pun','gas'):
                    lista_definitiva.append(elemento)
        df_puntoscarga_reduced["num_electricPump"] = np.random.randint(1, 3, df_puntoscarga_reduced.shape[0])
        df_puntoscarga_reduced["num_electricPump"][df_puntoscarga_reduced['id'].isin(lista_definitiva)] = 3
        rendimiento_carga = 0.9
        if tipo_programa != "GASOLINERA":
            #Para los puntos de recarga, hay datos disponibles para el cálculo
            logger.info("Calculo tiempo de parada para puntos de recarga")
            tiempos_puntos_parada_pc = []
            tiempos_puntos_espera_pc = []
            capacidad_coche = float(df_electricar["BATTERY_CAPACITY"])*1000 #Wh
            for index, punto_carga in df_puntoscarga_reduced.iterrows():
                numero_conectores_pc = int(punto_carga["num_connectors"])
                if numero_conectores_pc == 1:
                    potencia_pc = 0.9*float(punto_carga["ratedPowerKW"])*1000 #W
                else:
                    conectores = punto_carga["connectorType"].split(",")
                    conectores_limpio = []
                    for elem in conectores:
                        conectores_limpio.append(re.sub('[^A-Za-z0-9]+', '', elem))
                    potencias = punto_carga["ratedPowerKW"].split(",")
                    potencias_limpio = []
                    for elem in potencias:
                        potencias_limpio.append(float(re.sub('[^0-9a-zA-Z.]+', '', elem)))
                    if tipo_conector != "":
                        indice = conectores_limpio.index(tipo_conector)
                    else:
                        maximo = max(potencias_limpio)
                        indice = potencias_limpio.index(max(potencias_limpio))
                    potencia_pc = float(potencias_limpio[indice])*1000 #W
                tiempos_puntos_parada_pc.append((punto_carga["id"],
                                              Tiempos.calcular_tiempo_parada(capacidad_coche,
                                                                             potencia_pc,
                                                                             punto_carga["id"],
                                                                             punto_carga["num_electricPump"],
                                                                             datetime.datetime.now(),
                                                                             lista_definitiva,
                                                                             rendimiento_carga)))
                tiempos_puntos_espera_pc.append((punto_carga["id"],
                                              Tiempos.calcular_tiempo_espera_cola(punto_carga["id"],
                                                                                 punto_carga["num_electricPump"],
                                                                                 datetime.datetime.now(),
                                                                                 lista_definitiva)))
            column_names = ["id","Parada_h"]
            df_tiempos_puntos_parada_pc = pd.DataFrame(data = tiempos_puntos_parada_pc, columns = column_names)
            column_names = ["id","Espera_h"]
            df_tiempos_puntos_espera_pc = pd.DataFrame(data = tiempos_puntos_espera_pc, columns = column_names)
        if tipo_programa != "PUNTO_RECARGA":
            #TODO: Para los gasolineras, hay que ver como se calculan los datos (nos lo inventamos?)
            tiempos_puntos_parada_gas = np.random.uniform(2, 5, df_gasolineras.shape[0])
            column_names = ["id","Parada_h"]
            df_tiempos_puntos_parada_gas = pd.DataFrame(columns = column_names)
            df_tiempos_puntos_parada_gas["id"] = df_gasolineras["id"]
            df_tiempos_puntos_parada_gas["Parada_h"] = tiempos_puntos_parada_gas
        if tipo_programa == "GASOLINERA":
            df_tiempos_puntos_parada = df_tiempos_puntos_parada_gas
        elif tipo_programa == "PUNTO_RECARGA":
            df_tiempos_puntos_parada = df_tiempos_puntos_parada_pc
        else:
            frames = [df_tiempos_puntos_parada_pc,df_tiempos_puntos_parada_gas]
            df_tiempos_puntos_parada = pd.concat(frames)
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
        path_coordinates = []
        total_tiempo = 0
        for index, lugar  in enumerate(path):
            if lugar in df_ciudades["id"].unique():
                coord = (float(df_ciudades["Latitude"][df_ciudades["id"]==lugar]),
                         float(df_ciudades["Longitude"][df_ciudades["id"]==lugar]))
            elif lugar in df_puntoscarga_reduced["id"].unique():
                coord = (float(df_puntoscarga_reduced["latitude"][df_puntoscarga_reduced["id"]==lugar]),
                         float(df_puntoscarga_reduced["longitude"][df_puntoscarga_reduced["id"]==lugar]))
            elif lugar in df_puntoscarga_reduced["id"].unique():
                coord = (float(df_gasolineras["latitud"][df_gasolineras["id"]==lugar]),
                         float(df_gasolineras["longitud"][df_gasolineras["id"]==lugar]))
            else:
                coord = (0,0)
            path_coordinates.append(coord)
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
        bd_output = BaseDatos.BaseDatos(host=db_host,
                                        puerto=3306,            
                                        usuario="root",            
                                        password="root",        
                                        basedatos="tfm") 
        logger.info("Crear conexion a DB")
        con = bd_output.crear_conexion()
        # Query a Output
        logger.info("Query a Output")
        sql_query_output = "INSERT INTO Output (user_id, timestamp, origen, destino, num_paradas, path, tiempo_total, tipo_programa, marca_coche, modelo_coche, carga_inicial, carga_final, tipo_conector) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        path_string = '-'.join(path)
        argumentos_output = (user_id,
                             datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             origen,
                             destino,
                             len(path)-2,
                             path_string,
                             total_tiempo,
                             tipo_programa,
                             marca_coche,
                             modelo_coche,
                             carga_inicial,
                             carga_final,
                             tipo_conector)
        rowcount = bd_output.ejecutar_queries_insert(con = con,
                                                     sql_query = sql_query_output,
                                                     argumentos = argumentos_output)
        logger.info("%s registros insertados.",rowcount)
        logger.info("Cerrar conexion con DB")
        con.close()
        logger.info("[OK] Final del script calcular_caminos_entre_puntos.py [OK]")
        return path_coordinates
    except:
        logger.error("[ERROR] El programa no ha podido obtener una ruta [ERROR]")
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
                        required = False,
                        type = str,
                        default = "",
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
    parser.add_argument("--user_id",
                        required = False,
                        default = 1,
                        type = int,
                        help = "Id del usuario "
                               "Default: 1")
    parser.add_argument("--use_docker",
                        required = False,
                        default = False,
                        type = bool,
                        help = "Usar Docker "
                               "Default: False")
    args = parser.parse_args()

    main_route(tipo_programa = args.tipo_programa,
               marca_coche = args.marca_coche,
               modelo_coche = args.modelo_coche,
               origen = args.origen,
               destino = args.destino,
               carga_inicial = args.carga_inicial,
               carga_final = args.carga_final,
               tipo_conector = args.tipo_conector,
               log_level = args.log_level,
               log_path = args.log_path,
               user_id = args.user_id,
               use_docker = args.use_docker)
    
