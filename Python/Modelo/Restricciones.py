# -*- coding: utf-8 -*-
import pandas as pd

def restriccion_tipo_conector(distancias, puntoscarga_reduced):
     """
    Definicion de la funcion restriccion_tipo_conector:
        
        Funcion de aplicar las restriccione tipo conector

    Parametros
    ----------
    distancias:            Pandas Dataframe
        Dataframe que contiene los resultados de la query
    
    puntoscarga_reduced:   list[string]
        Lista de string que contiene los id de los puntos de carga
        con el tipo de conector necesario
    
    Returns
    ------
    restriccion_tipo_conector_df:   Pandas Dataframe
            Pandas Dataframe que contiene restriccion tipo conector
    
    Ejemplo
    -------
    >>> restriccion_tipo_conector = Restricciones.restriccion_tipo_conector(distancias = df_distancias_pc,
                                                                            puntoscarga_reduced = puntoscarga_reduced)
    """
     restriccion_tipo_conector = []
     for index, distancia in distancias.iterrows():
        if ("punto_recarga" in distancia["Origen"]) & ("punto_recarga" in distancia["Destino"]):
            if (distancia["Origen"] in puntoscarga_reduced) & (distancia["Destino"] in puntoscarga_reduced):
                restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],True))
            else:
                restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],False))
        else:
            if (distancia["Origen"] in puntoscarga_reduced) | (distancia["Destino"] in puntoscarga_reduced):
                restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],True))
            else:
                restriccion_tipo_conector.append((distancia["Origen"],distancia["Destino"],False))
     column_names = ["Origen","Destino","Restr_con"]
     restriccion_tipo_conector_df = pd.DataFrame(data = restriccion_tipo_conector, columns = column_names)
     return restriccion_tipo_conector_df

def restriccion_primera_parada(distancias_origen, carga_inicial, autonomia_coche):
     """
    Definicion de la funcion restriccion_primera_parada:
        
        Funcion de aplicar la restriccion de primera parada

    Parametros
    ----------
    distancias_origen:     Pandas Dataframe
        Dataframe que contiene las distancias desde el origen
    
    carga_inicial:         float
        Porcentaje de carga inicial del coche al iniciar el viaje
    
    autonomia_coche:       float
        Autonomia del coche 
    
    Returns
    ------
    restriccion_tipo_conector_df:   Pandas Dataframe
            Pandas Dataframe que contiene restriccion tipo conector
    
    Ejemplo
    -------
    >>> restricciones_prim_par = Restricciones.restriccion_primera_parada(distancias_origen = df_distancias_origen,
                                                                          carga_inicial = float(args.carga_inicial),
                                                                          autonomia_coche = autonomia_coche)
    """
     restriccion_primera_parada = []
     for index, distancia in distancias_origen.iterrows():
        if (float(distancia["Distance_km"]) - 0.9 * autonomia_coche * carga_inicial / 100) <= 0:
            restriccion_primera_parada.append((distancia["Origen"],distancia["Destino"],True))
        else:
            restriccion_primera_parada.append((distancia["Origen"],distancia["Destino"],False))
     column_names = ["Origen","Destino","Restr_prim_par"]
     restriccion_primera_parada_df = pd.DataFrame(data = restriccion_primera_parada, columns = column_names)
     return restriccion_primera_parada_df

def restriccion_ultima_parada(distancias_destino, carga_final, autonomia_coche):
     """
    Definicion de la funcion restriccion_ultima_parada:
        
        Funcion de aplicar la restriccion de ultima parada

    Parametros
    ----------
    distancias_destino:     Pandas Dataframe
        Dataframe que contiene las distancias desde el destino
    
    carga_final:            float
        Porcentaje de carga final del coche al iniciar el viaje
    autonomia_coche:        float
        Autonomia del coche        
     
    Returns
    ------
    restriccion_tipo_conector_df:   Pandas Dataframe
            Pandas Dataframe que contiene restriccion tipo conector
    
    Ejemplo
    -------
    >>> restricciones_ult_par = Restricciones.restriccion_ultima_parada(distancias_destino = df_distancias_destino,
                                                                        carga_final = float(args.carga_final),
                                                                        autonomia_coche = autonomia_coche)
    """
     restriccion_ultima_parada = []
     for index, distancia in distancias_destino.iterrows():
        if (float(distancia["Distance_km"]) - ((100 - carga_final) / 100 * 0.9 * autonomia_coche)) <= 0:
            restriccion_ultima_parada.append((distancia["Origen"],distancia["Destino"],True))
        else:
            restriccion_ultima_parada.append((distancia["Origen"],distancia["Destino"],False))
     column_names = ["Origen","Destino","Restr_ult_par"]
     restriccion_ultima_parada_df = pd.DataFrame(data = restriccion_ultima_parada, columns = column_names)
     return restriccion_ultima_parada_df