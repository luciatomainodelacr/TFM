# -*- coding: utf-8 -*-
import networkx as nx

# TODO: Para todas las funciones de este fichero hay que repasar cuales son necesarias y 
# cuales no y , en casa de dejarlas, documentarlas
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

        for weight in ["time"]:
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


