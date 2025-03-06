import json
import read_GIPS_distance  # ✅ 新增：導入 UWB 讀取模組

def get_uwb_position():
    """✅ 新增函數：從 UWB 讀取測距數據並返回座標"""
    uwbpos = read_GIPS_distance.UWBpos()
    position = uwbpos.compute_CRS()  # 使用 compute_CRS() 計算座標
    print(f"📍 UWB 讀取位置: {position}")
    return position

def findRoute(st=[], dest=[]):
    print(dest, type(dest), "dest")

    # ✅ 如果 st 沒有提供，則從 UWB 讀取當前位置
    if not st:
        st = get_uwb_position()

    if dest == []:
        return []

    global graph
    graph = Graph(10)

    # load information from json file
    with open('points.json', 'r') as file:
        data = json.load(file)

    # add vertex data
    graph.add_vertex_data(0, st)
    graph.add_vertex_data(9, dest)
    for node in data['cross']:
        graph.add_vertex_data(node['id'], node['pos'])

    # add edges (original cross)
    for i in range(1, 9):
        for k in range(i + 1, 9):
            if k-i == 1 or k-i == 4:
                if k != 5 or i != 4:
                    print(i, k)
                    len = ((graph.vertex_data[i][0] - graph.vertex_data[k][0])**2 +
                           (graph.vertex_data[i][1] - graph.vertex_data[k][1])**2)**0.5
                    graph.add_edge(i, k, len)
            else:
                graph.add_edge(i, k, 0)

    print(graph.adj_matrix)

    # add edges (st and dest)
    addEdge(0, 9, data)
    for i in range(1, 9):
        addEdge(0, i, data)
        addEdge(9, i, data)

    route = graph.dijkstra(st)
    finalRoute = []
    for i in route:
        finalRoute.append(graph.vertex_data[i])

    print(finalRoute)
    return finalRoute

if __name__ == "__main__":
    # ✅ 設定目標位置（目的地）
    destination = [25.1045, 121.2773]

    # ✅ 執行 `findRoute`，如果沒有提供 `st`，則從 UWB 讀取
    findRoute(dest=destination)
