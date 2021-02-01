# -*- coding: utf-8 -*-
def calcular_tiempo_recorrido(distancias, velocidad):
     """
    Definicion de la funcion calcular_tiempo_recorrido:
        
        Funcion de calculo del tiempo de recorrido 

    Parametros
    ----------
    distancias:            Pandas Dataframe
        Dataframe que contiene las distancias entre nodos
    
    velocidad:             float
        float con velocidad media del coche
    
    Returns
    ------
    tiempos_recorrido:      Pandas Dataframe
            Pandas Dataframe que el tiempo de recorrido para cada arista
    
    Ejemplo
    -------
    >>> df_distancias_reduced["Time_h"] = Tiempos.calcular_tiempo_recorrido(df_distancias_reduced["Distance_km"],velocidad_coche)
    """
     tiempos_recorrido = distancias/velocidad
     return tiempos_recorrido


def calcular_tiempo_parada(capacidad_bateria, potencia_pc, numero_conectores_pc):
     """
    Definicion de la funcion calcular_tiempo_parada:
        
        Funcion de calculo del tiempo de parada

    Parametros
    ----------
    distancias:            Pandas Dataframe
        Dataframe que contiene las distancias entre nodos
    
    capacidad_bateria:             float
        float con capacidad de bateria para el coche
    
    potencia_pc:             float
        float con potencia para el punto de carga
    
    numero_conectores_pc:    float
        float con numero de conectores para el punto de carga
    
    Returns
    ------
    tiempo_parada:           float
            Tiempo de parada para ese punto y coche
    
    Ejemplo
    -------
    >>> tiempos_puntos_parada.append((punto_carga["id"],Tiempos.calcular_tiempo_parada(capacidad_coche,potencia_pc,numero_conectores_pc)))
    """
     tiempo_recarga = calcular_tiempo_recarga(potencia_pc,capacidad_bateria)
     tiempo_espera = calcular_tiempo_espera(numero_conectores_pc)
     tiempo_parada = tiempo_recarga + tiempo_espera
     return tiempo_parada


def calcular_tiempo_recarga(potencia_pc,capacidad_bateria):
    #TODO: Implementar calculo mas complejo de tiempo de recarga
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