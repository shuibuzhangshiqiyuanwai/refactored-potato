import pandas as pd
import numpy as np
import folium
import plotly.express as px
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import warnings
warnings.filterwarnings('ignore')


# 读取所有中间文件
rawData = pd.read_csv('cleaned_data.csv', parse_dates=['Date', 'Time'])
year_counts = pd.read_csv('year_counts.csv')
month_counts = pd.read_csv('month_counts.csv')
day_counts = pd.read_csv('day_counts.csv')
province_counts = pd.read_csv('china_province_counts.csv')
world_type_counts = pd.read_csv('world_type_counts.csv')
china_type_counts = pd.read_csv('china_type_counts.csv')
top500_mag = pd.read_csv('top500_magnitude.csv', parse_dates=['Date', 'Time'])
top500_depth = pd.read_csv('top500_depth.csv', parse_dates=['Date', 'Time'])
mag_depth = pd.read_csv('magnitude_depth.csv')

# 中国境内数据（Area 非空的记录）
china_data = rawData[rawData['Area'].notna()].copy()


#可视化



#所有地震地图
m = folium.Map(location=[20, 0], zoom_start=2)
for _, row in rawData.iterrows():
    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
        radius = np.exp(row['Magnitude']) / 100
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=min(radius, 15),
            color='red',
            fill=True,
            fill_opacity=0.6,
            popup=f"Mag: {row['Magnitude']}, Depth: {row['Depth']}"
        ).add_to(m)
m.save('all_earthquakes_map.html')

#年、月、日次数图
fig_year = px.bar(year_counts, x='Year', y='Count', title='每年地震次数')
fig_year.write_html('year_counts.html')

fig_month = px.bar(month_counts, x='Month', y='Count', title='每月地震次数')
fig_month.write_html('month_counts.html')

fig_day = px.bar(day_counts, x='Day', y='Count', title='每日地震次数')
fig_day.write_html('day_counts.html')

#中国境内 1955-2016 省份分布
china_1955_2016 = china_data[(china_data['Year'] >= 1955) & (china_data['Year'] <= 2016)]
m_china = folium.Map(location=[35, 105], zoom_start=4)
for a, row in china_1955_2016.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=3,
        color='blue',
        fill=True,
        popup=f"Area: {row['Area']}"
    ).add_to(m_china)
m_china.save('china_earthquakes_1955_2016.html')

# 省份柱状图
province_plot_data = china_1955_2016['Area'].value_counts().reset_index()
province_plot_data.columns = ['Province', 'Count']
fig_prov = px.bar(province_plot_data, x='Province', y='Count',
                  title='1955-2016 中国各省地震次数')
fig_prov.write_html('china_province_bar.html')

# 词云图
wordcloud_data = [(row['Province'], row['Count']) for a, row in province_plot_data.iterrows()]
wc = (
    WordCloud()
    .add(series_name="省份", data_pair=wordcloud_data, word_size_range=[20, 100])
    .set_global_opts(title_opts=opts.TitleOpts(title="中国各省地震词云"))
)
wc.render('china_province_wordcloud.html')

#震级前500地图
m_top500_mag = folium.Map(location=[20, 0], zoom_start=2)
for _, row in top500_mag.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Magnitude'] * 2,
        color='darkred',
        fill=True,
        popup=f"Mag: {row['Magnitude']}, Date: {row['Date']}"
    ).add_to(m_top500_mag)
m_top500_mag.save('top500_magnitude_map.html')

#深度前500地图
m_top500_depth = folium.Map(location=[20, 0], zoom_start=2)
for _, row in top500_depth.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Depth'] / 20,
        color='purple',
        fill=True,
        popup=f"Depth: {row['Depth']}, Mag: {row['Magnitude']}"
    ).add_to(m_top500_depth)
m_top500_depth.save('top500_depth_map.html')

#饼图
fig_world_pie = px.pie(world_type_counts, values='Count', names='Type',
                       title='世界范围地震类型分布')
fig_world_pie.write_html('world_type_pie.html')

fig_china_pie = px.pie(china_type_counts, values='Count', names='Type',
                       title='中国境内地震类型分布')
fig_china_pie.write_html('china_type_pie.html')

#震级-深度散点图
fig_scatter = px.scatter(mag_depth, x='Depth', y='Magnitude',
                         title='震级 vs 震源深度', opacity=0.5)
fig_scatter.write_html('magnitude_depth_scatter.html')

print("所有可视化已完成，HTML 文件已生成。")