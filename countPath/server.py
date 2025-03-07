from flask import Flask, request, jsonify
from flask_cors import CORS
from findRoute import findRoute
from read_GIPS_distance import UWBpos

app = Flask(__name__)
CORS(app)

pos = UWBpos()

@app.route('/dest', methods=['POST'])  # ✅ 確保這裡是 `POST`
def dest():
    print('📡 `/dest` 收到請求...')

    # ✅ 確保 `request.json` 存在且包含 `dest`
    if not request.json or 'dest' not in request.json:
        print("❌ 錯誤: `dest` 參數缺失")
        return jsonify({"error": "Missing `dest` parameter"}), 400

    destination = request.json['dest']
    st = request.json.get('st', None)  # 允許 `st` 為空（可從 UWB 讀取）

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

if __name__ == "__main__":
    print("🚀 啟動 Flask 伺服器，監聽 0.0.0.0:5500")
    app.run(host="0.0.0.0", port=5500, debug=True)
