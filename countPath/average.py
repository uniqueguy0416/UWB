import csv
import numpy as np
from time import sleep
from read_GIPS_distance import UWBpos  # 將這行改成你目前檔名，例如 uwb_module.py

# 測試參數
actual_distance_cm = 700  # 輸入你預設的真實距離
measure_times = 20

uwb = UWBpos()
results = []

print("🔍 開始測距...")

for i in range(measure_times):
    dis_to_anchor = uwb.UWB_read()
    dist = dis_to_anchor[0]  # anchor6
    print(f"第 {i+1} 次：距離 = {dist:.2f} cm")
    results.append(dist)
    sleep(0.2)

mean = np.mean(results)
error = mean - actual_distance_cm
std = np.std(results)

print("\n📊 測試結果：")
print(f"平均距離 = {mean:.2f} cm")
print(f"誤差 = {error:.2f} cm")
print(f"標準差 = {std:.2f} cm")

# 儲存結果
with open("uwb_precision_test.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["測距次數", "距離 (cm)"])
    for i, d in enumerate(results):
        writer.writerow([i+1, d])

print("✅ 結果已儲存到 uwb_precision_test.csv")
