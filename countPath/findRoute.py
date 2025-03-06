import json
import read_GIPS_distance  # 只加上這一行來讀取 UWB 位置

def findRoute(st=[], dest=[]):
    print(dest, type(dest), "dest")

    if not dest:
        return []

    global graph
    graph = Graph(10)

    # 讀取 `points.json`
    with open('points.json', 'r') as file:
        data = json.load(file)

    # 確保 `st` 來自 UWB 測量
    if not st:
        uwbpos = read_GIPS_distance.UWBpos()
        st = uwbpos.compute_CRS()  # 獲取當前 UWB 座標
        print(f"📍 UWB 當前位置: {st}")

    # 設定起點與終點
    graph.add_vertex_data(0, st)
    graph.add_vertex_data(9, dest)

    for node in data['cross']:
        graph.add_vertex_data(node['id'], node['pos'])

    # 建立圖的連結
    for i in range(1, 9):
        for k in range(i + 1, 9):
            if k - i == 1 or k - i == 4:
                if k != 5 or i != 4:
                    distance = ((graph.vertex_data[i][0] - graph.vertex_data[k][0]) ** 2 +
                                (graph.vertex_data[i][1] - graph.vertex_data[k][1]) ** 2) ** 0.5
                    graph.add_edge(i, k, distance)
            else:
                graph.add_edge(i, k, 0)

    print(graph.adj_matrix)

    # 設定起點與終點的邊
    addEdge(0, 9, data)
    for i in range(1, 9):
        addEdge(0, i, data)
        addEdge(9, i, data)

    # 執行 Dijkstra 找最短路徑
    route = graph.dijkstra(st)

    # 轉換為 GPS 座標
    finalRoute = [graph.vertex_data[i] for i in route]

    print("🛤️ 最短路徑:", finalRoute)
    return finalRoute

if __name__ == "__main__":
    # 目標位置（終點）
    destination = [25.1045, 121.2773]

    # 執行 `findRoute`，UWB 位置自動填入
    findRoute(dest=destination)
