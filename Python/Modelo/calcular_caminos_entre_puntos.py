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

# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Python/Modelo/')
import ModeloAvanzado.funcion_aux as fa


# 2.- Funcion main ------------------------------------------------
#------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("""ERROR: Este programa necesita 9 parametros: nombre_programa
            tipo_programa marca_coche modelo_coche origen destino carga_inicial 
            carga_final  tipo_conector""")
        sys.exit(1)
    else:
        print("The number of arguments is ", len(sys.argv))
        program_name = sys.argv[0]
        # program type can be: "GASOLINERA, PUNTO_RECARGA, ALL"
        program_type = sys.argv[1]
        car_brand = sys.argv[2]
        car_model = sys.argv[3]
        origin = sys.argv[4]
        destination = sys.argv[5]
        initial_charge = float(sys.argv[6])
        final_charge = float(sys.argv[7])
        connector_type = sys.argv[8]
        print("El programa lanzado es: ",program_name, program_type,
        car_brand, car_model, origin, destination, initial_charge, 
        final_charge, connector_type)

    try:

        # 1.- Carga de inputs ---------------------------------------------
        #------------------------------------------------------------------

        # Crear conexion a la base de datos 
        con = mysql.connector.connect(host="localhost",
                                    port=3306,            
                                    user="root",            
                                    password="root",        
                                    database="tfm")

        cur = con.cursor()

        sql_query = "SELECT * FROM PuntosCarga"
        cur.execute(sql_query)
        df_puntoscarga = pd.DataFrame(cur.fetchall(), columns = ["id","latitude","longitude","name","streetName","provincia","ccaa","postalCode","connectorType","ratedPowerKW","num_connectors","status"])

        sql_query = "SELECT * FROM Ciudades"
        cur.execute(sql_query)
        df_ciudades = pd.DataFrame(cur.fetchall(), columns = ["id","PROVINCIA","ADDRESS","Latitude","Longitude","COORDENADAS","status"])

        df_ciudades.set_index(["id"], inplace=True)
        df_ciudades.drop("status",axis="columns", inplace=True)

        sql_query = "SELECT * FROM ElectricCar WHERE BRAND = %s AND MODEL = %s"
        arg = (car_brand,car_model)
        cur.execute(sql_query, arg)
        df_electricar = pd.DataFrame(cur.fetchall(), columns = ["BRAND","MODEL","RANGE_KM","EFFICIENCY_WHKM","FASTCHARGE_KMH","RAPIDCHARGE","PLUGTYPE", "BATTERY_CAPACITY"])
        autonomia_coche = 0.9*float(df_electricar["RANGE_KM"])

        #La restriccion de autonomi�a se aplica directamente en la llamada a la query
        if program_type == "GASOLINERA":
            sql_query = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'gasolinera%' AND Destino LIKE 'gasolinera%') OR (Origen LIKE %s AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'gasolinera%' AND Destino LIKE %s));"
            arg = (autonomia_coche,origin,destination)
            cur.execute(sql_query, arg)
            df_distancias = pd.DataFrame(cur.fetchall(), columns = ["Origen","Destino","Distance_km"])
        elif program_type == "PUNTO_RECARGA":
            sql_query = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'punto_recarga%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'punto_recarga%') OR (Origen LIKE 'punto_recarga%' AND Destino LIKE %s));"
            arg = (autonomia_coche,origin,destination)
            cur.execute(sql_query, arg)
            df_distancias = pd.DataFrame(cur.fetchall(), columns = ["Origen","Destino","Distance_km"])
        else:
            sql_query = "SELECT * FROM Matriz_distancia_haversine WHERE Distance_km <= %s AND ((Origen LIKE 'gasolinera%' AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'punto_recarga%' AND  Destino LIKE 'gasolinera%') OR (Origen LIKE 'gasolinera%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE 'punto_recarga%' AND  Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'punto_recarga%') OR (Origen LIKE %s AND Destino LIKE 'gasolinera%') OR (Origen LIKE 'punto_recarga%' AND Destino LIKE %s) OR (Origen LIKE 'gasolinera%' AND Destino LIKE %s));"
            arg = (autonomia_coche,origin,origin,destination,destination)
            cur.execute(sql_query, arg)
            df_distancias = pd.DataFrame(cur.fetchall(), columns = ["Origen","Destino","Distance_km"])
        con.close()

        # Filtrar el df_distancias con las restricciones del Modelo Avanzado

        # a) Restriccion de tipo de conector
        puntoscarga_reduced = []
        for index, punto_carga in df_puntoscarga.iterrows():
            if connector_type in punto_carga["connectorType"]:
                puntoscarga_reduced.append(str(punto_carga["id"]))
        df_puntoscarga_reduced = df_puntoscarga[df_puntoscarga["id"].isin(puntoscarga_reduced)]

        df_distancias_pc = df_distancias[(df_distancias["Origen"].str.contains("punto_recarga"))|(df_distancias["Destino"].str.contains("punto_recarga"))]
        restriccion_tipo_conector = fa.restriccion_tipo_conector(df_distancias_pc,puntoscarga_reduced)

        # b) Restriccion de primera parada
        df_distancias_origen = df_distancias[df_distancias["Origen"]==origin]
        restricciones_prim_par = fa.restriccion_primera_parada(df_distancias_origen,initial_charge,autonomia_coche)

        # c) Restriccion de ultima parada
        df_distancias_destino = df_distancias[df_distancias["Destino"]==destination]
        restricciones_ult_par = fa.restriccion_ultima_parada(df_distancias_destino,final_charge,autonomia_coche)

        # Se genera el dataframe reducido que cumple con todas las restricciones
        df_distancias_merged_1 = pd.merge(df_distancias, restriccion_tipo_conector, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged_2 = pd.merge(df_distancias_merged_1, restricciones_prim_par, on=['Origen', 'Destino'], how='outer')
        df_distancias_merged = pd.merge(df_distancias_merged_2, restricciones_ult_par, on=['Origen', 'Destino'], how='outer')
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

