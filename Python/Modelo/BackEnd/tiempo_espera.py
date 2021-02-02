

# Se cargan las librerias
import numpy as np
import pandas as pd
import os


# 1.- Carga de Inputs ---------------------------------------------
#------------------------------------------------------------------

# Se importa el csv que contiene toda la combinatoria de distancias
df = pd.read_csv('/home/tfm/Documentos/TFM/Datasets/Matriz_Distancias/matriz_distancia_haversine.csv', sep=';', encoding='unicode_escape', header=0)

# Compruebo tipologia de cada variable
df.dtypes

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


len(lista_definitiva)
len(puntos_50km_ciud)

    
        

        
      

