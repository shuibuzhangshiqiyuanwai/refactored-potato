import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime


# 读取原始数据 包含列: Date, Time, Latitude, Longitude, Magnitude, Depth, Type
rawData = pd.read_csv('earthquake.csv')
# 清洗 Date 和 Time
rawData['Structed Date'] = pd.to_datetime(rawData['Date'],
                                          format='%m/%d/%Y',
                                          errors='coerce').dt.date

failed_date_idx = rawData[rawData['Structed Date'].isnull()].index    # 找到解析失败的行
print('无法解析的日期索引:', failed_date_idx.tolist())

fix_list = [3378, 7512, 20650]   # 手动修正特定行（原数据中这三个日期无法自动转换）
for idx in fix_list:
    if idx in rawData.index:
        rawData.loc[idx, 'Structed Date'] = pd.to_datetime(rawData.loc[idx, 'Date']).date()

rawData.loc[3378, 'Structed Date'] = datetime(1975, 2, 23).date()
rawData.loc[7512, 'Structed Date'] = datetime(1985, 4, 28).date()
rawData.loc[20650, 'Structed Date'] = datetime(2011, 3, 13).date()
del rawData['Date']
rawData['Structed Time'] = pd.to_datetime(rawData['Time'],   # 清洗 Time
                                          format='%H:%M:%S',
                                          errors='coerce').dt.time
failed_time_idx = rawData[rawData['Structed Time'].isnull()].index
print('无法解析的时间索引:', failed_time_idx.tolist())
# 手动修正
rawData.loc[3378, 'Structed Time'] = pd.to_datetime('2:58:41', format='%H:%M:%S').time()
rawData.loc[7512, 'Structed Time'] = pd.to_datetime('2:53:41', format='%H:%M:%S').time()
rawData.loc[20650, 'Structed Time'] = pd.to_datetime('2:23:34', format='%H:%M:%S').time()
del rawData['Time']

# 重命名列
rawData.rename(columns={'Structed Date': 'Date', 'Structed Time': 'Time'}, inplace=True)


# 2. 高德逆地理编码，根据经纬度获取地名

AMAP_KEY = '9d0b8972c105cec1891eef47ea9763cf'

def get_province(lon, lat):

    url = 'https://restapi.amap.com/v3/geocode/regeo'
    params = {
        'output': 'json',
        'location': f'{lon},{lat}',
        'key': AMAP_KEY
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        #print(res.text)   # 调试用，查看完整的返回内容
        data = res.json()

        if data['status'] == '0':
            print(f'请求失败，错误信息：{data.get("info")}')
            return None
        addr = data['regeocode']['addressComponent']
        addr = data.get('regeocode', {}).get('addressComponent', {})
        country = addr.get('country')
        if country == '中国':
            province = addr.get('province')
            # 过滤掉“中华人民共和国”这类非省级名称
            if province and province not in ['中华人民共和国', '中国', '']:
                return province
            sea = addr.get('seaArea')
            if sea:
                return sea
        return None

    except Exception as e:
        print(f'请求异常：{e}')
        return None
    return None

# def get_province(lon, lat):
#     u1 = 'http://restapi.amap.com/v3/geocode/regeo?output=json&'
#     key = AMAP_KEY
#     location = 'location=' + str(lon) + ',' + str(lat)
#     url = u1 + location + key
#     res = requests.get(url)
#     json_data = json.loads(res.text)
#     regeoinfo = json_data['regeocode']['addressComponent']
#
#     if 'country' in regeoinfo and regeoinfo['country'] == '中国':
#         if 'province' in regeoinfo and regeoinfo['province']:
#             return regeoinfo['province']
#         elif 'seaArea' in regeoinfo and regeoinfo['seaArea']:
#             return regeoinfo['seaArea']
#
#     return None


# for i in range(23412):
#     lon = rawData.loc[i, 'Longitude']
#     lat = rawData.loc[i, 'Latitude']
#     rawData.loc[i, 'Area'] = getProvince(lon, lat)
# def get_province(lon, lat):
#     if AMAP_KEY == '你的高德Key':
#         return None  # 没有 Key 时直接返回空
#     url = 'https://restapi.amap.com/v3/geocode/regeo'
#     params = {
#         'output': 'json',
#         'location': f'{lon},{lat}',
#         'key': AMAP_KEY
#     }
#     try:
#         res = requests.get(url, params=params, timeout=5)
#         data = res.json()
#         addr = data['regeocode']['addressComponent']
#         if addr.get('country') == '中国':
#             return addr.get('province') or addr.get('seaArea')
#     except:
#         pass
#     return None
try:
   for i in rawData.index:
      lon = rawData.at[i, 'Longitude']
      lat = rawData.at[i, 'Latitude']
      rawData.at[i, 'Area'] = get_province(lon, lat)


      if i % 100 == 0:
        print(f'已处理 {i} 行...')
        time.sleep(0.001)  # 防止请求过快
        print('Area 唯一值:', rawData['Area'].dropna().unique())
   print('Area 唯一值:', rawData['Area'].dropna().unique())
except Exception as e:
    print(f'请求异常：{e}')


# 按年、月、日分开保存

rawData['Year'] = rawData['Date'].apply(lambda x: x.year)
rawData['Month'] = rawData['Date'].apply(lambda x: x.month)
rawData['Day'] = rawData['Date'].apply(lambda x: x.day)

year_cnt = rawData['Year'].value_counts().sort_index().reset_index()
year_cnt.columns = ['Year', 'Count']
month_cnt = rawData['Month'].value_counts().sort_index().reset_index()
month_cnt.columns = ['Month', 'Count']
day_cnt = rawData['Day'].value_counts().sort_index().reset_index()
day_cnt.columns = ['Day', 'Count']

year_cnt.to_csv('year_counts.csv', index=False)
month_cnt.to_csv('month_counts.csv', index=False)
day_cnt.to_csv('day_counts.csv', index=False)


# 中国境内每个省份（海域）发生重大地震的次数

china_data = rawData[rawData['Area'].notna()].copy()
province_cnt = china_data['Area'].value_counts().reset_index()
province_cnt.columns = ['Province', 'Count']
province_cnt.to_csv('china_province_counts.csv', index=False)


# 不同类型地震的数量（中国境内 & 世界）

# 世界范围
world_type_cnt = rawData['Type'].value_counts().reset_index()
world_type_cnt.columns = ['Type', 'Count']
world_type_cnt.to_csv('world_type_counts.csv', index=False)

# 中国境内
china_type_cnt = china_data['Type'].value_counts().reset_index()
china_type_cnt.columns = ['Type', 'Count']
china_type_cnt.to_csv('china_type_counts.csv', index=False)


# 震级前 500 的地震

top500_mag = rawData.sort_values(['Magnitude', 'Date'],
                                 ascending=[False, False]).head(500)
top500_mag.to_csv('top500_magnitude.csv', index=False)


# 震源深度前 500 的地震（深度相同按震级降序）

top500_depth = rawData.sort_values(['Depth', 'Magnitude'],
                                   ascending=[False, False]).head(500)
top500_depth.to_csv('top500_depth.csv', index=False)


# 震级与震源深度关系数据

mag_depth = rawData[['Magnitude', 'Depth']].dropna()
mag_depth.to_csv('magnitude_depth.csv', index=False)


# 保存清洗后的完整数据
rawData.to_csv('cleaned_data.csv', index=False)

# 保存按年/月/日计数
year_cnt.to_csv('year_counts.csv', index=False)
month_cnt.to_csv('month_counts.csv', index=False)
day_cnt.to_csv('day_counts.csv', index=False)

# 保存中国各省份（海域）地震次数
province_cnt.to_csv('china_province_counts.csv', index=False)

# 保存世界和中国境内地震类型统计
world_type_cnt.to_csv('world_type_counts.csv', index=False)
china_type_cnt.to_csv('china_type_counts.csv', index=False)

# 保存震级前500和深度前500
top500_mag.to_csv('top500_magnitude.csv', index=False)
top500_depth.to_csv('top500_depth.csv', index=False)

# 保存震级与深度关系
mag_depth.to_csv('magnitude_depth.csv', index=False)