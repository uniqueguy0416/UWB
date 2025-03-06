import json
import read_GIPS_distance  # ✅ 確保讀取 `UWB` 資料

def get_uwb_position():
    """✅ 讀取 UWB 位置，並確保返回有效數據"""
    print("📡 嘗試讀取 UWB 位置...")
    try:
        uwbpos = read_GIPS_distance.UWBpos()
        position = uwbpos.compute_CRS()  # UWB 計算座標
        print(f"📍 讀取成功！UWB 位置: {position}")
        return position
    except Exception as e:
        print(f"❌ UWB 讀取失敗: {e}")
        return []

def findRoute(st=[], dest=[]):
    print(dest, type(dest), "dest")

    # ✅ 如果 st 沒有提供，則從 UWB 讀取當前位置
    if not st:
        st = get_uwb_position()
        if not st:
            print("❌ 錯誤: 無法讀取 UWB 位置，無法計算路徑")
            return []

    if dest == []:
        print("❌ 錯誤: 目標位置 `dest` 為空，請提供有效座標")
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
    destination = [25.1045, 121.2773]  # 目標位置
    print(f"🎯 設定的目標位置: {destination}")

    findRoute(dest=destination)
