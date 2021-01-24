#Importar librerias
import pandas as pd

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

def calcular_tiempo_parada(potencia_punto,capacidad_bateria, numero_conectores_pc):
    tiempo_recarga = calcular_tiempo_recarga_B(potencia_punto,capacidad_bateria)
    tiempos_espera = []
    for numero_conectores_pc_1 in numero_conectores_pc:
        tiempos_espera.append(calcular_tiempo_espera(numero_conectores_pc_1))
    tiempo_espera = sum(tiempos_espera)
    tiempo_parada = tiempo_recarga + tiempo_espera
    return tiempo_parada


# OPCION A
def calcular_tiempo_recarga_A(carga, distancias):
    tiempo_recarga = carga * (len(distancias)-1) # (tiempo de carga * numero de paradas)
    return tiempo_recarga

# OPCION B
def calcular_tiempo_recarga_B(potencia_punto,capacidad_bateria):
    tiempo_recarga = []
    for potencia_punto in potencia_punto:
        tiempo_recarga.append(capacidad_bateria / potencia_punto)
    tiempo_recarga = sum(tiempo_recarga)
    return tiempo_recarga




# ANOTACIONES TIEMPO DE RECARGA:
# Va a depender de:
# 1)Como de cargado este el coche --> vamos a suponer una cte de 10% de bateria
# 2)Tipo de carga que ofrezca el punto de carga --> una potencia concreta






def calcular_tiempo_espera(numero_conectores_1pc):
    #TODO: Habría que calcular el tiempo de espera en función del número de conectores del punto de recarga
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






#Restricciones: autonomía real

def restriccion_autonomia(distancias, autonomia_coche):
    restriccion_autonomia = []
    for index, distancia in distancias.iterrows():
        if (float(distancia["Distance_km"]) - 0.9 * autonomia_coche) <= 0:
            restriccion_autonomia.append((distancia["Origen"],distancia["Destino"],True))
        else:
            restriccion_autonomia.append((distancia["Origen"],distancia["Destino"],False))
    column_names = ["Origen","Destino","Restr_aut"]
    restriccion_autonomia_df = pd.DataFrame(data = restriccion_autonomia, columns = column_names)
    return restriccion_autonomia_df




def restriccion_primera_parada(distancias_origen, carga_inicial, autonomia_coche):
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
    restriccion_ultima_parada = []
    for index, distancia in distancias_destino.iterrows():
        if (float(distancia["Distance_km"]) - ((100 - carga_final) / 100 * 0.9 * autonomia_coche)) <= 0:
            restriccion_ultima_parada.append((distancia["Origen"],distancia["Destino"],True))
        else:
            restriccion_ultima_parada.append((distancia["Origen"],distancia["Destino"],False))
    column_names = ["Origen","Destino","Restr_ult_par"]
    restriccion_ultima_parada_df = pd.DataFrame(data = restriccion_ultima_parada, columns = column_names)
    return restriccion_ultima_parada_df




