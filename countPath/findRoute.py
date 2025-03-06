import json
import read_GIPS_distance  # 引入 UWB 讀取模組

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
        if start_vertex_data not in self.vertex_data:
            print("❌ 錯誤: 起點不在圖中")
            return []

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

        # 動態設定終點
        target = self.size - 1
        route = [target]
        for i in range(len(tempRoute) - 1, -1, -1):
            if tempRoute[i][1] == target:
                target = tempRoute[i][0]
                route.append(target)
            if target == 0:
                break

        return route

# 檢查兩條線是否相交
def checkIntersection(A, B, C, D):
    a1 = B[1] - A[1]
    b1 = A[0] - B[0]
    c1 = a1 * A[0] + b1 * A[1]

    a2 = D[1] - C[1]
    b2 = C[0] - D[0]
    c2 = a2 * C[0] + b2 * C[1]

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        return None  # 平行線

    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant

    if (
        min(A[0], B[0]) <= x <= max(A[0], B[0])
        and min(A[1], B[1]) <= y <= max(A[1], B[1])
        and min(C[0], D[0]) <= x <= max(C[0], D[0])
        and min(C[1], D[1]) <= y <= max(C[1], D[1])
    ):
        return True
    return False

# 新增邊，確保不會與障礙物相交
def addEdge(st, dst, data):
    inter = False
    for box in data["box"]:
        if inter:  # 如果找到交叉就跳出
            break
        for k in range(4):
            if checkIntersection(
                graph.vertex_data[st], graph.vertex_data[dst], box["edge"][k], box["edge"][(k + 1) % 4]
            ):
                graph.add_edge(st, dst, 0)
                inter = True
                break

    if not inter:
        distance = ((graph.vertex_data[st][0] - graph.vertex_data[dst][0]) ** 2 +
                    (graph.vertex_data[st][1] - graph.vertex_data[dst][1]) ** 2) ** 0.5
        graph.add_edge(st, dst, distance)

# 主要函數：計算最短路徑
def findRoute():
    global graph

    # 讀取當前 UWB 位置
    uwbpos = read_GIPS_distance.UWBpos()
    start_position = uwbpos.compute_CRS()  # 取得 UWB 計算的座標

    # 設定目標位置
    destination = [25.1045, 121.2773]  # 目標座標

    if not start_position or not destination:
        print("❌ 錯誤: 起點或終點無效")
        return []

    print(f"📍 UWB 當前位置: {start_position}")
    print(f"🎯 目標位置: {destination}")

    # 讀取 `points.json`
    with open("points.json", "r") as file:
        data = json.load(file)

    # 動態設定圖的大小
    num_cross = len(data["cross"])
    graph = Graph(num_cross + 2)

    # 設定起點與終點
    graph.add_vertex_data(0, start_position)
    graph.add_vertex_data(num_cross + 1, destination)

    # 設定交叉點
    for node in data["cross"]:
        graph.add_vertex_data(node["id"], node["pos"])

    # 設定邊
    for i in range(1, num_cross + 1):
        for k in range(i + 1, num_cross + 1):
            if k - i == 1 or k - i == 4:
                distance = ((graph.vertex_data[i][0] - graph.vertex_data[k][0]) ** 2 +
                            (graph.vertex_data[i][1] - graph.vertex_data[k][1]) ** 2) ** 0.5
                graph.add_edge(i, k, distance)

    # 設定起點與終點的邊
    addEdge(0, num_cross + 1, data)
    for i in range(1, num_cross + 1):
        addEdge(0, i, data)
        addEdge(num_cross + 1, i, data)

    # 執行 Dijkstra 找最短路徑
    route = graph.dijkstra(start_position)

    # 轉換為 GPS 座標
    finalRoute = [graph.vertex_data[i] for i in route]
    print("🛤️ 最短路徑:", finalRoute)

    return finalRoute

if __name__ == "__main__":
    findRoute()
