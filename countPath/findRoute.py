import json
import read_GIPS_distance  # ✅ 新增：導入 UWB 讀取模組

# ✅ 確保 `Graph` 類別已經定義，避免 `NameError`
class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [[]] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # 無向圖

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dijkstra(self, start_vertex_data):
        start_vertex = self.vertex_data.index(start_vertex_data)
        distances = [float('inf')] * self.size
        distances[start_vertex] = 0
        visited = [False] * self.size

        tempRoute = []
        nodeList = [i for i in range(self.size)]
        for _ in range(self.size):
            min_distance = float('inf')
            u = None
            for i in range(self.size):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    u = i
            if u is None:
                break

            visited[u] = True
            tempRoute.append((nodeList[u], u))

            for v in range(self.size):
                if self.adj_matrix[u][v] != 0 and not visited[v]:
                    alt = distances[u] + self.adj_matrix[u][v]
                    if alt < distances[v]:
                        distances[v] = alt
                        nodeList[v] = u

        target = 9
        route = [target]
        for i in range(len(tempRoute)-1, -1, -1):
            if tempRoute[i][1] == target:
                target = tempRoute[i][0]
                route.append(target)
            if target == 0:
                break

        return route
