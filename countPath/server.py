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
    print("✅ [Flask] /pos 被呼叫了")
    try:
        print("➡️ 開始使用 fake_read()")
        pos.fake_read()
        print("✅ fake_read() 完成")

        print("➡️ 開始 compute_CRS()")
        x, y = pos.compute_CRS()
        print(f"✅ compute_CRS() 完成，結果為：({y}, {x})")

        return jsonify([x, y]), 200
    except Exception as e:
        print("❌ /pos 發生錯誤：", e)
        return jsonify({"error": str(e)}), 200



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
