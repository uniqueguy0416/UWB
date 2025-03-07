import json
import requests  # ✅ 用於從 `server.py` 獲取 `destination`

class Graph:
    def __init__(self, size):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_data = [[]] * size

    def add_edge(self, u, v, weight):
        if 0 <= u < self.size and 0 <= v < self.size:
            self.adj_matrix[u][v] = weight
            self.adj_matrix[v][u] = weight  # For undirected graph

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
            tempRoute.append((nodeList[u], u))
            if u is None:
                break

            visited[u] = True

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
        print("🛤 計算出的路徑:", route)

        return route

# ✅ 獲取 `server.py` 提供的 `destination`
def get_destination():
    url = "http://127.0.0.1:5500/dest"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            destination = response.json()
            print(f"✅ 從 `server.py` 取得目標位置: {destination}")
            return destination
        else:
            print(f"❌ 無法從 `server.py` 取得目標位置，錯誤碼: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ 錯誤: 無法請求 `server.py`，錯誤訊息: {e}")
        return []

def findRoute(st=[], dest=[]):
    print(f"📍 起點 (st): {st}")
    print(f"🎯 目標位置 (dest): {dest}, 類型: {type(dest)}")

    if not dest:
        print("❌ 錯誤: 目標位置 `dest` 為空，無法計算路徑")
        return []

    global graph
    graph = Graph(10)

    # 讀取 `points.json` 文件，確保節點資訊正確
    with open('points.json', 'r') as file:
        data = json.load(file)

    # ✅ 確保 `st` 和 `dest` 被加入圖中
    graph.add_vertex_data(0, st)
    graph.add_vertex_data(9, dest)
    for node in data['cross']:
        graph.add_vertex_data(node['id'], node['pos'])

    # ✅ 設定圖的邊
    for i in range(1, 9):
        for k in range(i + 1, 9):
            if k-i == 1 or k-i == 4:
                if k != 5 or i != 4:
                    print(f"📌 設置邊: {i} <-> {k}")
                    length = ((graph.vertex_data[i][0] - graph.vertex_data[k][0])**2 +
                              (graph.vertex_data[i][1] - graph.vertex_data[k][1])**2)**0.5
                    graph.add_edge(i, k, length)
            else:
                graph.add_edge(i, k, 0)

    # ✅ 計算最短路徑
    route = graph.dijkstra(st)
    finalRoute = [graph.vertex_data[i] for i in route]

    print("🚀 計算出的最佳路徑:", finalRoute)
    return finalRoute

if __name__ == "__main__":
    # ✅ 從 `server.py` 獲取 `destination`
    destination = get_destination()
    print(f"🎯 目標位置: {destination}")

    # ✅ 確保 `findRoute()` 獲取 `destination`
    route = findRoute(dest=destination)

    print("🚀 最終計算出的最佳路徑:")
    print(route)
