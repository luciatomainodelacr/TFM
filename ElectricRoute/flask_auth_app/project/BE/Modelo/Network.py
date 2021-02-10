# -*- coding: utf-8 -*-
import networkx as nx

def show_path(DG,path):
     """
    Definicion del procedimiento show_path:
        
        Procedimiento para mostrar la duracion completa del trayecto 

    Parametros
    ----------
    DG:             DiGraph
        Grafo con la red de nodos y aristas de la red de puntos de 
        recarga, gasolineras y ciudades
    
    path:           list[string]
        Lista que contiene los puntos por los que se pasa en el 
        trayecto
        
    Returns
    ------
    Al ser un procedimiento, no hay un return, si no que se realizan
    las operaciones dentro
    
    Ejemplo
    -------
    >>> show_path(DiGraph,path)
    """
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
     """
    Definicion del procedimiento get_all_shortest_paths:
        
        Procedimiento para obtener los caminos más cortos posibles 

    Parametros
    ----------
    DiGraph:        DiGraph
        Grafo con la red de nodos y aristas de la red de puntos de 
        recarga, gasolineras y ciudades
    
    origen:         string
        String que contiene la ciudad origen del camino

    destino:        string
        String que contiene la ciudad destino del camino

    Returns
    ------
    Al ser un procedimiento, no hay un return, si no que se realizan
    las operaciones dentro
    
    Ejemplo
    -------
    >>> Network.get_all_shortest_paths(DG, origen = origen, destino = destino)
    """
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


def get_shortest_path(DiGraph, origen, destino):
     """
    Definicion del procedimiento get_shortest_path:
        
        Procedimiento para obtener el camino más corto 

    Parametros
    ----------
    DiGraph:        DiGraph
        Grafo con la red de nodos y aristas de la red de puntos de 
        recarga, gasolineras y ciudades
    
    origen:         string
        String que contiene la ciudad origen del camino

    destino:        string
        String que contiene la ciudad destino del camino

    Returns
    ------
    Al ser un procedimiento, no hay un return, si no que se realizan
    las operaciones dentro
    
    Ejemplo
    -------
    >>> Network.get_shortest_path(DG, origen = origen, destino = destino)
    """
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


