import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_csv(file_path="sample_flight_data.csv"):
    # 1. 生成时间序列 (每隔1分钟记录一次，共2小时数据)
    start_time = datetime.now() - timedelta(hours=2)
    timestamps = [start_time + timedelta(minutes=i) for i in range(120)]
    
    # 2. 模拟飞行高度 (ft)：起飞 -> 巡航 -> 降落
    altitude = np.concatenate([
        np.linspace(0, 35000, 30),  # 起飞爬升阶段
        np.full(60, 35000) + np.random.normal(0, 200, 60), # 巡航阶段 (带细微波动)
        np.linspace(35000, 0, 30)   # 降落阶段
    ])
    
    # 3. 模拟飞行速度 (kts)
    airspeed = np.concatenate([
        np.linspace(0, 450, 30),
        np.full(60, 460) + np.random.normal(0, 10, 60),
        np.linspace(450, 0, 30)
    ])
    
    # 4. 模拟经纬度 (假设一条简单的航线)
    latitude = np.linspace(39.9042, 31.2304, 120)  # 北京 -> 上海 纬度变化
    longitude = np.linspace(116.4074, 121.4737, 120)
    
    # 5. 模拟垂直速度 (fpm)，并加入一些异常值
    vertical_speed = np.zeros(120)
    vertical_speed[0:30] = 1200  # 爬升
    vertical_speed[90:120] = -1200 # 下降
    # 随机加入一些异常颠簸
    vertical_speed[45] = 2500
    vertical_speed[72] = -3000
    
    # 6. 模拟发动机温度 (正常范围 + 一个告警异常)
    engine_temp = np.random.normal(850, 20, 120)
    engine_temp[60] = 1050  # 制造一个温度异常点
    
    # 7. 组装 DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'altitude_ft': altitude.round(0),
        'airspeed_kts': airspeed.round(1),
        'latitude': latitude.round(6),
        'longitude': longitude.round(6),
        'vertical_speed_fpm': vertical_speed,
        'engine_temp_c': engine_temp.round(1)
    })
    
    # 8. 保存为 CSV
    df.to_csv(file_path, index=False)
    print(f"✅ 示例 CSV 文件已生成: {file_path}")
    print(f"   共包含 {len(df)} 行飞行数据")

if __name__ == "__main__":
    generate_sample_csv()
