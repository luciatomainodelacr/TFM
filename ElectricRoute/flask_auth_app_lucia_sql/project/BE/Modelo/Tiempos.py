# -*- coding: utf-8 -*-
import datetime

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


def calcular_tiempo_parada(capacidad_bateria, potencia_pc, punto_recarga, num_electricPump, timestamp, lista_definitiva, rendimiento_carga):
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
    >>> tiempos_puntos_parada.append((punto_carga["id"],
    Tiempos.calcular_tiempo_parada(capacidad_coche,potencia_pc,numero_conectores_pc)))
    """
     tiempo_recarga = calcular_tiempo_recarga(potencia_pc, capacidad_bateria, rendimiento_carga)
     tiempo_espera = calcular_tiempo_espera_cola(punto_recarga, num_electricPump, timestamp, lista_definitiva)
     tiempo_parada = tiempo_recarga + tiempo_espera
     return tiempo_parada

# ANOTACIONES TIEMPO DE RECARGA:
# Va a depender de:
# 1)Como de cargado este el coche --> vamos a suponer una cte de 10% de bateria
# 2)Tipo de carga que ofrezca el punto de carga --> una potencia concreta

def calcular_tiempo_recarga(potencia_pc, capacidad_bateria, rendimiento_carga):
     """
    Definicion de la funcion calcular_tiempo_recarga:
        
        Funcion de calculo del tiempo de recarga para un coche 
        y punto de recarga especifico

    Parametros
    ----------
    potencia_pc:             float
        Float con la potencia del punto de carga
    
    capacidad_bateria:       float
        Float con capacidad de bateria para el coche
    
    rendimiento_carga:       float
        Float con el rendimiento del proceso de carga
    
    Returns
    ------
    tiempo_recarga:          float
            Tiempo de recarga para ese punto y coche
    
    Ejemplo
    -------
    >>> tiempo_recarga = calcular_tiempo_recarga(potencia_pc, 
                                                 capacidad_bateria,
                                                 rendimiento_carga)
    """
     tiempo_recarga = capacidad_bateria / (potencia_pc * rendimiento_carga)
     return tiempo_recarga


def calcular_tiempo_espera_cola(punto_recarga, num_electricPump, timestamp, lista_definitiva):
     """
    Definicion de la funcion calcular_tiempo_espera_cola:
        
        Funcion de calculo del tiempo de espera segun la 
        teoria de colas en un punto de recarga especifico

    Parametros
    ----------
    punto_recarga:            string
        String con el id del punto de recarga
    
    num_electricPump:         int
        Int con el número de surtidores del punto de recarga
    
    timestamp:                datetime
        Datetime de la hora de la consulta
    
    lista_definitiva:         list[string]
        Lista de ids de los puntos de recarga/gasolineras a 
        menos de 50 km de una ciudad importante
    
    Returns
    ------
    tiempo_espera_cola:       float
            Tiempo de espera de cola para ese punto y coche
    
    Ejemplo
    -------
    >>> tiempo_espera = calcular_tiempo_espera_cola(punto_recarga,
                                                    num_electricPump,
                                                    timestamp,
                                                    lista_definitiva)
    """
     landa1 = valor_lambda(punto_recarga, timestamp, lista_definitiva)
     mu = 3
     factor_congestion = landa1 / (num_electricPump * mu)

     inicio = 0
     final = num_electricPump - 1
     def sumatorio(inicio,final):
        control = 0
        n = range(0, final + 1)
        for x in n:
            control += pow((landa1/mu),x) / factorial(x) + (1/factorial(num_electricPump)) * pow((landa1/mu),num_electricPump) * (1/(1-factor_congestion))
        return control
    
     probab_no_cola = 1 / sumatorio(inicio,final)
     num_usuarios_cola = pow((landa1/mu),num_electricPump) * landa1 * mu / (factorial(final) * pow((num_electricPump*mu-landa1),2)) * probab_no_cola
     tiempo_espera_cola = num_usuarios_cola / landa1
    
     return tiempo_espera_cola

def valor_lambda(punto_recarga, timestamp, lista_definitiva):
     """
    Definicion de la funcion valor_lambda:
        
        Funcion de calculo del parámetro lambda de la teoría
        de colas 

    Parametros
    ----------
    punto_recarga:            string
        String con el id del punto de recarga
    
    timestamp:                datetime
        Datetime de la hora de la consulta
    
    lista_definitiva:         list[string]
        Lista de ids de los puntos de recarga/gasolineras a 
        menos de 50 km de una ciudad importante
    
    Returns
    ------
    landa:                    int
          Parámetro lambda de la teoría de colas para cálculo
          de tiempo de espera
    
    Ejemplo
    -------
    >>> landa1 = valor_lambda(punto_recarga, timestamp, lista_definitiva)
    """
     # Obtenemos hora y mes actuales (instante en que usuario realiza su consulta)
     hora = timestamp.hour
     mes = timestamp.month
     horario_diurno = list(range(7,23))
     periodo_vacacional = list(range(5,10))
     if punto_recarga in lista_definitiva:
        if hora in horario_diurno:
            if mes in periodo_vacacional:
                landa = 8
            else:
                landa = 4
        elif mes in periodo_vacacional:
            landa = 4
        else:
            landa = 2

     elif hora in horario_diurno:
        if mes in periodo_vacacional:
            landa = 2
        else:
            landa = 1
     elif mes in periodo_vacacional:
        landa = 1
     else:
        landa = 1
        
     return landa



# Funcion para calcular el factorial de un numero entero
def factorial(entero): 
     """
    Definicion de la funcion factorial:
        
        Funcion de calculo del factorial de un numero entero

    Parametros
    ----------
    entero:            int
        Entero del que calcular el factorial para cálculo de
        tiempo de espera
    
    Returns
    ------
    resultado:         int
        Entero con el factorial de entero
    
    Ejemplo
    -------
    >>> num_usuarios_cola = pow((landa1/mu),num_electricPump) * landa1 * mu 
    / (factorial(final) * pow((num_electricPump*mu-landa1),2)) * probab_no_cola
    """
     resultado = 1
     i = 1
     while i <= entero:
        resultado = resultado * i
        i = i + 1
     return resultado
