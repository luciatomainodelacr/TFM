import numpy as np
from _graph.DynamicGraph import DynamicGraph


class GraphAPSP(DynamicGraph):

    def __init__(self, source=[], target=[], weight=[], directed=True):
        DynamicGraph.__init__(self, source, target, weight, directed)

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

        return dist

    def apsp_dijkstra(self):

        result = np.full((self.vertex.size, self.vertex.size), np.inf)
        count = 0
        for v in self.vertex:
            result[count] = self.sssp_dijkstra(v)
            count = count + 1

        return result

    def floyd_warshall(self):

        total_vertex = len(self.vertex)
        dist = np.zeros((total_vertex, total_vertex))
        dist.fill(np.inf)

        for idx in range(self.source.size):
            index_s = self.vertex == self.source[idx]
            index_t = self.vertex == self.target[idx]
            dist[index_s, index_t] = self.weight[idx]
        for index in range(self.vertex.size):
            dist[index, index] = 0

        for k in np.nditer(self.vertex):
            for i in np.nditer(self.vertex):
                for j in np.nditer(self.vertex):
                    index_k = self.vertex == k
                    index_i = self.vertex == i
                    index_j = self.vertex == j

                    if dist[index_i, index_j] > dist[index_i, index_k] + dist[index_k, index_j]:
                        dist[index_i, index_j] = dist[index_i, index_k] + dist[index_k, index_j]

        return dist
