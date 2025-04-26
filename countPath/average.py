import csv
import numpy as np
from time import sleep
from read_GIPS_distance import UWBpos  # 根據你的檔名修改

# ✅ 設定參數
actual_distance_cm = 2000  # 真實距離（cm）
measure_times = 20  # 測量次數

uwb = UWBpos()
results = []

print(f"📏 測試 anchor6 與目標間距離，預設真實距離為 {actual_distance_cm} cm")
print("🔍 開始測距...\n")

for i in range(measure_times):
    dis_to_anchor = uwb.UWB_read()  # 回傳格式：如 [713, 687, 50]

    # 只取第 0 個（anchor6）
    raw_value = dis_to_anchor[0]
    print(f"dis[0] read: {raw_value}")

    # 判斷單位：大於 10 通常為 cm，小於 10 為 m
    if raw_value > 10:
        dist_cm = raw_value
    else:
        dist_cm = raw_value * 100

    # 忽略異常值
    if dist_cm < 1:
        print(f"⚠️ 第 {i+1} 次無效資料（{dist_cm:.2f} cm），跳過\n")
        sleep(0.2)
        continue

    print(f"✅ 第 {i+1} 次距離：{dist_cm:.2f} cm\n")
    results.append(dist_cm)
    sleep(0.2)

# 統計分析
mean = np.mean(results)
error = mean - actual_distance_cm
std = np.std(results)

print("📊 測試結果統計：")
print(f"🔢 有效測距次數：{len(results)}")
print(f"📏 平均距離：{mean:.2f} cm")
print(f"📉 誤差：{error:.2f} cm")
print(f"📐 標準差：{std:.2f} cm\n")

# 存檔
with open("uwb_precision_test.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["測距次數", "距離 (cm)"])
    for i, d in enumerate(results):
        writer.writerow([i + 1, d])

print("✅ 測距結果已儲存到：uwb_precision_test.csv")
