from flask import Flask, request, jsonify
from flask_cors import CORS
from findRoute import findRoute
from read_GIPS_distance import UWBpos

app = Flask(__name__)
CORS(app)

# ✅ 初始化 UWB 位置物件
pos = UWBpos()

# ✅ `/dest` 端點 - 接收目標位置並計算路徑
@app.route('/dest', methods=['POST'])
def dest():
    print('📡 `/dest` 收到請求...')

    if not request.json or 'dest' not in request.json:
        print("❌ 錯誤: `dest` 參數缺失")
        return jsonify({"error": "Missing `dest` parameter"}), 400

    destination = request.json['dest']
    st = request.json.get('st', None)  # 允許 st 為空（可從 UWB 讀取）

    print(f"🎯 目標位置: {destination}")
    print(f"📍 起點: {st if st else '從 UWB 讀取'}")

    # ✅ 如果 `st` 為空，則從 UWB 讀取當前位置
    if not st:
        st = pos.UWB_read_compute_CRS_5()
        print(f"📍 讀取 UWB 當前位置: {st}")

    route = findRoute(st, destination)
    response_data = {"route": route}

    print(f"🚀 計算出的最佳路徑: {route}")
    return jsonify(response_data), 200

# ✅ `/pos` 端點 - 取得 UWB 當前座標
@app.route('/pos')
def getPos():
    print("📡 `/pos` 被請求，讀取 UWB 位置...")

    pos.UWB_read()  # 讀取 UWB 數據
    x, y = pos.UWB_read_compute_CRS_5()

    print(f"✅ 當前 UWB 位置: {y}, {x}")
    return jsonify([x, y]), 200

# ✅ `/pos/anchor/<anchor_number>` 端點 - 取得指定 Anchor 座標
@app.route('/pos/anchor/<anchor_number>')
def getAnchorPos(anchor_number):
    print(f"📡 `/pos/anchor/{anchor_number}` 被請求...")
    x, y = pos.get_anchor_CRS(anchor_number)
    print(f"✅ Anchor {anchor_number} 位置: {x}, {y}")
    return jsonify([x, y]), 200

# ✅ `/pos/recalibrate` 端點 - 重新校正 UWB
@app.route('/pos/recalibrate')
def recalibrate():
    print("📡 `/pos/recalibrate` 被請求，開始重新校正 UWB...")
    x, y = pos.recalibrate()
    print(f"✅ 重新校正完成: x={x}, y={y}")
    return jsonify([x, y]), 200

# ✅ 啟動 Flask 伺服器
if __name__ == "__main__":
    print("🚀 啟動 Flask 伺服器，監聽 0.0.0.0:5500")
    app.run(host="0.0.0.0", port=5500, debug=True)
