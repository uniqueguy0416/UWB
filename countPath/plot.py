import serial
import binascii
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 🧠 若使用 SSH/無螢幕請啟用這行
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime

# ---------- UWB 參數 ----------
COM_PORT = '/dev/ttyUSB0'
BAUD_RATE = 57600
ANCHOR_ID = '0241000000000000'
MEASURE_TIMES = 20

# ---------- 提取距離 ----------
def swap_endian(hexstring):
    ba = bytearray.fromhex(hexstring)
    ba.reverse()
    return ba.hex()

def read_distance(ser):
    rx = ser.read(66)
    rx = binascii.hexlify(rx).decode('utf-8')

    if ANCHOR_ID in rx and rx.find(ANCHOR_ID) <= len(rx) - 24:
        idx = rx.find(ANCHOR_ID)
        dis = rx[idx+16:idx+24]
        dis = swap_endian(dis)
        try:
            val = int(dis, 16)
            return 0 if val >= 32768 else val / 100  # 公分
        except:
            return 0
    return 0

# ---------- 主測試函式 ----------
def test_and_save(actual_distance_cm):
    # 建立唯一時間戳記
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"output/uwb_precision_{timestamp}.csv"
    output_img = f"output/plot_uwb_result_{timestamp}.png"

    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    distances = []

    print(f"開始測試（實際距離：{actual_distance_cm} cm）")

    for i in range(MEASURE_TIMES):
        d = read_distance(ser)
        if d > 0:
            distances.append(d)
            print(f"{i+1:>2}/{MEASURE_TIMES}: {d:.2f} cm")
        else:
            print(f"{i+1:>2}/{MEASURE_TIMES}: 無效值，跳過")
        time.sleep(0.2)

    ser.close()

    avg = np.mean(distances)
    err = avg - actual_distance_cm
    std = np.std(distances)

    print(f"\n✅ 測試完成")
    print(f"平均值: {avg:.2f} cm")
    print(f"誤差:   {err:.2f} cm")
    print(f"標準差: {std:.2f} cm")

    # 儲存成 CSV
    os.makedirs("output", exist_ok=True)
    df = pd.DataFrame({
        "測試次數": list(range(1, len(distances)+1)),
        "距離 (cm)": distances
    })
    df_summary = pd.DataFrame([{
        "實際距離(cm)": actual_distance_cm,
        "平均距離(cm)": round(avg, 2),
        "誤差(cm)": round(err, 2),
        "標準差": round(std, 2)
    }])
    df_summary.to_csv(output_csv, index=False)

    # 畫圖儲存
    plt.figure(figsize=(8, 5))
    plt.plot(df["測試次數"], df["距離 (cm)"], marker='o')
    plt.axhline(actual_distance_cm, color='green', linestyle='--', label=f"實際距離: {actual_distance_cm}cm")
    plt.axhline(avg, color='blue', linestyle='--', label=f"平均距離: {avg:.2f}cm")
    plt.title("UWB 測距結果分析")
    plt.xlabel("測試次數")
    plt.ylabel("距離 (cm)")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_img)
    print(f"📊 圖片已儲存：{output_img}")
    print(f"📄 測試資料已儲存：{output_csv}")

# ---------- 主程式 ----------
if __name__ == "__main__":
    try:
        d = float(input("請輸入測試點實際距離（cm）："))
        if d > 0:
            test_and_save(d)
        else:
            print("❗請輸入大於 0 的距離")
    except Exception as e:
        print("錯誤：", e)
