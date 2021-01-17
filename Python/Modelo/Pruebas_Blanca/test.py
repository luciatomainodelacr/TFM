
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

df_ciudades = pd.read_csv(os.path.join(os.getcwd(),'ciudades_distancia.csv'), sep = ';', encoding = 'iso-8859-1', decimal = '.')

# Backup 
df = df_ciudades
df


list_origen = df["Origen"].unique()

list_fin = []
list_ciudad = []


def extrer_provincia(lugares, Origen, Distancia):
    x = ''
    for j in list_origen:

        if j == Origen:
            list.append(Distancia)

    return list


lista_dista = df.apply(lambda a: extrer_provincia(list_origen, a['formatted_address']), axis = 1)
























# 2.- Grafos ------------------------------------------------------
#------------------------------------------------------------------


# 3.- Algoritmo de Dijkstra ---------------------------------------
#------------------------------------------------------------------
class GraphPro(GraphAPSP):
    
    def __init__(self, source=[], target=[], weight=[], directed=True):
        GraphAPSP.__init__(self, source, target, weight, directed)

    @staticmethod
    def creategraph(total_nodes, pro_edges, weights, directed=True):

        source = np.array([])
        target = np.array([])
        weight = np.array([])

        for i in range(total_nodes):
            for k in range(i+1, total_nodes):
                if k == i:
                    continue

                p = 1 - pro_edges
                has_edge = np.random.choice(2, 1, p=[p, pro_edges])[0]

                if not has_edge:
                    continue

                probabilities = np.zeros(len(weights))
                probabilities = probabilities + (1 / len(weights))
                w = np.random.choice(weights, 1, p=probabilities)[0]

                source = np.append(source, i)
                target = np.append(target, k)
                weight = np.append(weight, w)

                if not directed:
                    source = np.append(source, k)
                    target = np.append(target, i)
                    weight = np.append(weight, w)

        return GraphPro(source, target, weight)

    def draw(self, with_weight=True):
        Gr = nx.DiGraph()
        Gr.add_weighted_edges_from(self.export())
        pos = nx.spring_layout(Gr)
        list_edges = list(Gr.edges())
        last = ()

        if self.last_vertex_modified.size > 0:
            last = (int(self.last_vertex_modified[0]), int(self.last_vertex_modified[1]) )
            list_edges.remove(last)

        nx.draw(Gr, pos=pos, with_labels=True, edgelist=list_edges, node_size=600)

        if with_weight:
            edge_labels = dict([((u, v,), d['weight']) for u, v, d in Gr.edges(data=True)])
            nx.draw_networkx_edge_labels(Gr, pos=pos, edgelist=list_edges, edge_labels=edge_labels)

        if len(last) > 0:
            nx.draw_networkx_edges(Gr, pos=pos, edgelist=[last], width=2.0, edge_color='b')

        plt.axis('off')
        plt.show()





# 3.- Algoritmo de Dijkstra ---------------------------------------
#------------------------------------------------------------------

def sssp_dijkstra(self, source):
    
    total_vertex = len(self.vertex)
    Q = np.array(self.vertex)

    dist = np.zeros(total_vertex)
    dist.fill(np.inf)

    dist[self.vertex == source] = 0

    while len(Q) != 0:

        min = np.inf
        u = 0
        for q in Q:
            if dist[self.vertex == q] <= min:
                min = dist[self.vertex == q]
                u = q

        Q = np.delete(Q, np.argwhere(Q == u))

        for v in self.target[self.source == u]:
            alt = dist[self.vertex == u] + self.get_weight(u, v)
            index_v = self.vertex == v
            if alt < dist[index_v]:
                dist[index_v] = alt


def apsp_dijkstra(self):
    
    result = np.full((self.vertex.size, self.vertex.size), np.inf)
    count = 0
    for v in self.vertex:
        result[count] = self.sssp_dijkstra(v)
        count = count + 1

    return result



from graph import GraphPro as g
from time import time
import os

os.system('clear')
print("<--------Test Dijkstra------->\n")

weights = [1, 2, 3, 4]
graph = GraphPro.creategraph(5, .75, weights, directed=False)
graph.print_r()
print('.........................')
t = time()
print(graph.apsp_dijkstra())
elapsed = time() - t
print("Time: ", elapsed)

graph.draw()

# Con df

weights = x
graph = GraphPro.creategraph(len(df), .75, weights, directed=False)
graph.print_r()
print('.........................')
t = time()
print(graph.apsp_dijkstra())
elapsed = time() - t
print("Time: ", elapsed)












#----------------------------------------------------------------------------------

sources = df["Origen"].tolist()
targets = df["Destino"].tolist()
weights = df["Distance_m"].tolist()

graph = Graph(sources, targets, weights)

graph.print_r()