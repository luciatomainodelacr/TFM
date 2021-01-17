# =============================================================================
#  MODELO DE OPTIMIZACION - CALCULA RUTA ENTRE DOS PUNTOS
# =============================================================================


# Se cargan las librerias
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import pandas as pd



# Se establece el diretorio base
os.chdir('/home/tfm/Documentos/TFM/Datasets/PuntosO_D/GeocodingAPI')


# 1.- Carga de inputs ---------------------------------------------
#------------------------------------------------------------------

df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'ciudades.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')
df_distancias = pd.read_csv(os.path.join(os.getcwd(),'ciudades_distancia.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')

# Backup 
df = df_distancias
df



# 2.- Grafo -------------------------------------------------------
#------------------------------------------------------------------

# Construir el grafo
DG = nx.DiGraph()

for row in df.iterrows():
    DG.add_edge(row[1]["Origen"],
                row[1]["Destino"],
                distance = row[1]["Distance_m"])

# Ver los nodos
DG.nodes(data = True)

# Graficamente
nx.draw_circular(DG,
                 node_color = 'lightblue',
                 edge_color = 'grey',
                 font_size = 24,
                 width = 2, with_labels = True, node_size = 3500)


list(nx.all_shortest_paths(DG, source = "Zaragoza Tren", target="Zamora Bus", weight=None))

list(nx.dijkstra_path(DG, source="Zaragoza Tren", target="Zamora Bus", weight=None))