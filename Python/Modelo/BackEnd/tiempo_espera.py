

# Se cargan las librerias
import numpy as np
import pandas as pd
import os
import datetime


# 1.- Carga de Inputs ---------------------------------------------
#------------------------------------------------------------------

# Se importa el csv que contiene toda la combinatoria de distancias
df = pd.read_csv('/home/tfm/Documentos/TFM/Datasets/Matriz_Distancias/matriz_distancia_haversine.csv', sep=';', encoding='unicode_escape', header=0)

# Filtro las distancias menores o iguales de 50 km entre las CIUDADES IMPORTANTES y 
# el resto de coordenadas

lista_ciudades_importantes = ["Madrid Tren", "Barcelona Tren", "Bilbao Tren", "Sevilla Tren", "Valencia Tren"]
puntos_50km_ciud = []
for ciudad in lista_ciudades_importantes:
    df1 = df[df["Origen"].str.contains(ciudad)]
    df1_50 = df1[df1['Distance_km']<= 50]
    for i in df1_50["Destino"]:
        puntos_50km_ciud.append(i)
    lista_definitiva = []
    for elemento in puntos_50km_ciud:
        if elemento[0:3] in ('pun','gas'):
            lista_definitiva.append(elemento)


len(lista_definitiva) # 98
len(puntos_50km_ciud) # 104

# La "lista_definitiva" contiene todos los puntos de recarga + gasolineras que distan igual o menos
# de 50 km de las grandes ciudades de España.



# Añadimos la columna "num_electricPump" que contenga el numero de surtidores electricos de cada 
# electrolinera. Puesto que no disponemos de la informacion, asignamos:

# 3 surtidores a todos los puntos de recarga a menos de 50 km de las grandes ciudades
# aleatoriamente valores entre [1,2] al resto de puntos de recarga

'''
df_puntos = pd.read_csv('/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/ptos_recarga_info.csv', sep=';', encoding='unicode_escape', header=0)
df_puntos["num_electricPump"] = np.random.randint(1, 4, df_puntos.shape[0])
df_puntos.to_csv('/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/ptos_recarga_info.csv', index=False)
'''

# Cargamos el csv de los puntos de recarga
df_puntos = pd.read_csv('/home/tfm/Documentos/TFM/Datasets/PuntosRecarga/ptos_recarga_info.csv', sep=';', encoding='unicode_escape', header=0)
df_puntos["num_electricPump"] = np.random.randint(1, 3, df_puntos.shape[0])


lista_indices = df_puntos[df_puntos['id'].isin(lista_definitiva)].index.tolist()
           
for indice in lista_indices:
    for i in df_puntos.iloc[indice]:

        


# El dia se divide en 2 franjas horarias: dia y noche.
# Si la hora de consulta del usuario esta entre:
# 7 am --> 10 pm (dia)
# 10 pm --> 7 am (noche)

# El año se divide en 2 periodos: vacacional e invernal
# Si la fecha de consulta del usuario se realiza en los meses:
# (Octubre - Abril) --> periodo invernal
# (Mayo - Septiembre) --> periodo_vacacional


# Nosotras conocemos la hora de salida del usuario:
# Para calcular la hora a la que llega a cada punto de recarga, debemos tener en cuenta la distancia
# recorrida desde el origen + el tiempo que permanece parado en el punto de recarga (tiempo de carga +
# tiempo de espera en la cola)

# Esta funcion nos devuelve el valor de lambda para cada punto de recarga donde para el conductor
# def valor_lambda(punto_recarga):
#     landa = 2
#     # Obtenemos hora y mes actuales (instante en que usuario realiza su consulta)
#     hora = datetime.datetime.now().hour
#     mes = datetime.datetime.now().month
#     horario_diurno = list(range(7,23))
#     periodo_vacacional = list(range(5,10))
#     if punto_recarga in lista_definitiva:
#         landa = landa * 2
#         if hora in horario_diurno:
#             landa = landa * 3
#             if mes in periodo_vacacional:
#                 landa = landa * 4
#     elif hora in horario_diurno:
#             landa = landa * 3
#             if mes in periodo_vacacional:
#                 landa = landa * 4
#     return landa



def valor_lambda(punto_recarga, hora):
    # Obtenemos hora y mes actuales (instante en que usuario realiza su consulta)
    #hora = datetime.datetime.now().hour
    mes = datetime.datetime.now().month
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

'''valor_lambda('punto_recarga_1', 1, 12)'''





# Funcion para calcular el factorial de un numero entero
def factorial(entero): 
    resultado = 1
    i = 1
    while i <= entero:
        resultado = resultado * i
        i = i + 1
    return resultado


# FUNCION QUE CALCULA EL TIEMPO DE ESPERA DE CADA USUARIO EN UN PUNTO DE RECARGA ESPECIFICO
def tiempo_espera_cola(punto_recarga, num_electricPump):
    landa1 = valor_lambda(punto_recarga)
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


tiempo_espera_cola('punto_recarga_1', 2)



