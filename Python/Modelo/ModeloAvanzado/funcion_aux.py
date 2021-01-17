#Importar librarias

#FUNCIONES

#Funcion objetivo: tiempo de de viaje
def funcion_objetivo_tiempo(distancias, velocidad, carga, numero_conectores_pc):
    tiempo_recorrido = calcular_tiempo_recorrido(distancias, velocidad)
    tiempo_parada = calcular_tiempo_parada(carga, distancias, numero_conectores_pc)
    tiempo_total = tiempo_recorrido + tiempo_parada
    return tiempo_total

def calcular_tiempo_recorrido(distancias, velocidad):
    distancia_recorrido = distancias.sum(axis = 0, skipna = True)
    tiempo_recorrido = distancia_recorrido/velocidad
    return tiempo_recorrido

def calcular_tiempo_parada(carga, distancias, numero_conectores_pc):
    tiempo_recarga = calcular_tiempo_recarga(carga, distancias)
    tiempos_espera = []
    for numero_conectores_pc_1 in numero_conectores_pc:
        tiempos_espera.append(calcular_tiempo_espera(numero_conectores_pc_1))
    tiempo_espera = sum(tiempos_espera)
    tiempo_parada = tiempo_recarga + tiempo_espera
    return tiempo_parada

def calcular_tiempo_recarga(carga, distancias):
    tiempo_recarga = carga * (len(distancias)-1)
    return tiempo_recarga

def calcular_tiempo_espera(numero_conectores_1pc):
    #TODO: Habría que calcular el tiempo de espera en función del número de conectores del punto de recarga
    tiempo_espera = 0.16 # en horas
    return tiempo_espera

#Restricciones: autonomía real

def restriccion_autonomia(distancias, autonomia_coche):
    restriccion_autonomia = []
    for distancia in distancias:
        if (distancia - autonomia_coche) <= 0:
            restriccion_autonomia.append(True)
        else:
            restriccion_autonomia.append(False)
    return restriccion_autonomia