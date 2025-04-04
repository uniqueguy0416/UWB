from flask import Flask, request, jsonify
from flask_cors import CORS
from findRoute import findRoute
from read_GIPS_distance import UWBpos

app = Flask(__name__)
CORS(app)
pos = UWBpos()

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
    try:
        # 模擬假資料（先用 fake_read 確認程式不卡）
        # pos.fake_read()  
        # x, y = pos.compute_CRS()

        # 實際用 UWB 定位（可能會卡住）
        pos.UWB_read()
        x, y = pos.UWB_read_compute_CRS_5()
        
        print(f"coordinate: {y}, {x}")
        return jsonify([x, y]), 200
    except Exception as e:
        print("❌ Error in /pos:", e)
        return jsonify({"error": str(e)}), 500

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
