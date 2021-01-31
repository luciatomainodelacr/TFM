#Importar librerias
import pandas as pd
import networkx as nx

#FUNCIONES

#Funcion objetivo: tiempo de viaje
def funcion_objetivo_tiempo(distancias, velocidad, carga, numero_conectores_pc):
    tiempo_recorrido = calcular_tiempo_recorrido(distancias, velocidad)
    tiempo_parada = calcular_tiempo_parada(carga, distancias, numero_conectores_pc)
    tiempo_total = tiempo_recorrido + tiempo_parada
    return tiempo_total


def calcular_tiempo_recorrido(distancias, velocidad):
    tiempos_recorrido = distancias/velocidad
    return tiempos_recorrido


def calcular_tiempo_parada(capacidad_bateria, potencia_pc, numero_conectores_pc):
    tiempo_recarga = calcular_tiempo_recarga(potencia_pc,capacidad_bateria)
    tiempo_espera = calcular_tiempo_espera(numero_conectores_pc)
    tiempo_parada = tiempo_recarga + tiempo_espera
    return tiempo_parada


def calcular_tiempo_recarga(potencia_pc,capacidad_bateria):
    tiempo_recarga = capacidad_bateria / potencia_pc
    return tiempo_recarga

# ANOTACIONES TIEMPO DE RECARGA:
# Va a depender de:
# 1)Como de cargado este el coche --> vamos a suponer una cte de 10% de bateria
# 2)Tipo de carga que ofrezca el punto de carga --> una potencia concreta


def calcular_tiempo_espera(numero_conectores_pc):
    #TODO: Habria que calcular el tiempo de espera en funcion del numero de conectores del punto de recarga
    tiempo_espera = 0.16 # en horas
    return tiempo_espera

# ANOTACIONES TIEMPO DE ESPERA:
# Va a depender de:
# 1)Numero de surtidores instalados --> posible variable inventada
# 2)Numero de coches que llegan en media a ese punto de recarga

# La 2) se puede plantear como una variable aleatoria que sigue una distribucion de Poisson y calcular su
# media. Una vez obtenido ese dato, establecer relacion con una distribucion exponencial negativa y, de
# ese modo, obtener probabilidad del tiempo de espera por coche. 

# Finalmente, podemos establecer un punto de corte y distinguir entre si la probabilidad de esperar es 
# mayor de 'tanto' fijar un tiempo de espera medio y si no otro


# Funcion que devuelve la duracion completa del trayecto 
def show_path(DG,path):
    try:
        total_tiempo = 0

        for i in range(len(path)-1):
            origen = path[i]
            destino = path[i+1]
            tiempo = DG[origen][destino]["time"]

            total_tiempo = total_tiempo + tiempo

            print(tiempo)        
    
        print("\n     Total Tiempo: %s h \n" % (total_tiempo))
    except:
        print("No hay ruta valida para ", path)

# Funcion que calcule todos los caminos posible y muestre los que tienen menor tiempo
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
                print("   Camino optimo: %s" % path)
                show_path(DiGraph,path)
    except:
        print("No hay ruta valida desde ", origen," hasta ", destino)


# Camino mas corto
def get_shortest_path(DiGraph, origen, destino):
    try:
        print("*** Origen: %s Destino: %s" % (origen, destino))

        for weight in ["tiempo"]:
            print(" Ordenado por: %s" % weight)
            path = list(nx.astar_path(DiGraph,
                                    (origen),
                                    (destino),
                                    weight = weight
                                    ))
            print("   Camino optimo: %s " % path)
            show_path(DiGraph,path)
    except:
            print("No hay ruta valida desde ", origen," hasta ", destino)


