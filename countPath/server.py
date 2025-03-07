from flask import Flask, request, jsonify
from threading import Thread
from flask_cors import CORS
from findRoute import findRoute
from read_GIPS_distance import UWBpos
app = Flask(__name__)
CORS(app)
pos = UWBpos()
# pos.recalibrate()


@app.route('/dest', methods=['POST'])
def dest():
    print('Destination received')
    print(request.json['dest'])

    route = findRoute(request.json['st'], request.json['dest'])
    response_data = {
        'route': route
    }
    return jsonify(response_data), 200


@app.route('/pos')
def getPos():
    print("call getPos")
    # pos.recalibrate()
    # pos.fake_read()     # if you don't have UWB module, use this
    pos.UWB_read()      # if you have UWB module, use this
    # x, y = pos.compute_CRS()
    x, y = pos.UWB_read_compute_CRS_5()
    # x, y = pos.get_anchor_CRS('9')
    print(f"coordinate: {y}, {x}")
    return jsonify([x, y]), 200


@app.route('/pos/anchor/<anchor_number>')
def getAnchorPos(anchor_number):
    x, y = pos.get_anchor_CRS(anchor_number)
    return jsonify([x, y]), 200


@app.route('/pos/recalibrate')
def recalibrate():
    x, y = pos.recalibrate()
    return jsonify([x, y]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)

app = Flask(__name__)
CORS(app)
pos = UWBpos()
# pos.recalibrate()


@app.route('/dest', methods=['POST'])
def dest():
    print('Destination received')
    print(request.json['dest'])

    route = findRoute(request.json['st'], request.json['dest'])
    response_data = {
        'route': route
    }
    return jsonify(response_data), 200


@app.route('/pos')
def getPos():
    # pos.recalibrate()
    # pos.fake_read()     # if you don't have UWB module, use this
    pos.UWB_read()      # if you have UWB module, use this
    # x, y = pos.compute_CRS()
    x, y = pos.UWB_read_compute_CRS_5()
    # x, y = pos.get_anchor_CRS('6')
    print(f"coordinate: {y}, {x}")
    return jsonify([x, y]), 200


@app.route('/pos/anchor/<anchor_number>')
def getAnchorPos(anchor_number):
    x, y = pos.get_anchor_CRS(anchor_number)
    return jsonify([x, y]), 200


@app.route('/pos/recalibrate')
def recalibrate():
    x, y = pos.recalibrate()
    return jsonify([x, y]), 200


if __name__ == "__main__":
    # 1️⃣ 先從 UWB 讀取目前的位置 (`st`)
    st = get_uwb_position()  # 這個函數應該從 `read_GIPS_distance.py` 取得 UWB 計算的座標
    print(f"📍 目前 UWB 位置: {st}")

    # 2️⃣ 向 `server.py` 取得 `destination`
    destination = get_destination()
    print(f"🎯 計算出的目標位置: {destination}")

    # 3️⃣ 執行 `findRoute()` 計算最短路徑
    route = findRoute(st=st, dest=destination)

    # 4️⃣ 顯示計算結果
    print("🚀 計算出的最佳路徑:")
    print(route)

