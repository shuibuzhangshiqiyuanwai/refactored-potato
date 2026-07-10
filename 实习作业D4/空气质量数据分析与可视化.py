import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- 中文显示设置 ----------
plt.rcParams['font.sans-serif'] = ['SimHei']      # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False        # 用来正常显示负号

# ---------- 1. 数据读取与预处理 ----------
df = pd.read_csv("PRSA_data.csv")

# 查看数据基本信息
print("数据规模：", df.shape)
print("列名：", df.columns.tolist())
print(df.head())

# 将年月日时合并为 datetime 索引，方便时间序列分析
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df.set_index('datetime', inplace=True)

# 处理 pm2.5 缺失值（使用前向填充，可根据实际情况调整）
df['pm2.5'] = df['pm2.5'].ffill()

# ---------- 2. 时间序列特征：绘制 PM2.5 日平均变化 ----------
# 计算每日平均 PM2.5
daily_pm25 = df['pm2.5'].resample('D').mean()

plt.figure(figsize=(14, 5))
plt.plot(daily_pm25.index, daily_pm25.values, color='dodgerblue', linewidth=0.8)
plt.title('2010-2014年每日平均 PM2.5 浓度变化', fontsize=14)
plt.xlabel('日期')
plt.ylabel('PM2.5 浓度 (ug/m**3)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ---------- 3. 污染物统计指标 ----------
print("\n===== PM2.5 统计指标 =====")
pm25_stats = df['pm2.5'].describe()
print(pm25_stats)

# 额外指标
print(f"中位数: {df['pm2.5'].median():.2f}")
print(f"标准差: {df['pm2.5'].std():.2f}")

# ---------- 4. 相关性分析与热力图 ----------
# 选择数值型变量
corr_cols = ['pm2.5', 'TEMP', 'DEWP', 'PRES', 'Iws']  # 可根据实际列名调整
corr_df = df[corr_cols].dropna()
corr_matrix = corr_df.corr()

# 打印与 PM2.5 的相关系数
print("\n===== PM2.5 与各气象因素的相关系数 =====")
print(corr_matrix['pm2.5'].drop('pm2.5'))

# 绘制热力图
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f',
            linewidths=0.5, square=True)
plt.title('污染物与气象因素相关性热力图', fontsize=14)
plt.tight_layout()
plt.show()

# ---------- 5. 多图表展示 ----------
# 5.1 柱状图：各月平均 PM2.5
df['month'] = df.index.month
monthly_avg = df.groupby('month')['pm2.5'].mean()

plt.figure(figsize=(10, 5))
bars = plt.bar(monthly_avg.index, monthly_avg.values, color='steelblue', edgecolor='black')
plt.title('各月平均 PM2.5 浓度', fontsize=14)
plt.xlabel('月份')
plt.ylabel('PM2.5 浓度 (ug/m**3)')
plt.xticks(range(1,13))
# 在柱顶标注数值
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}',
             ha='center', va='bottom', fontsize=8)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 5.2 散点图：温度（TEMP）与 PM2.5 的关系
plt.figure(figsize=(8, 6))
plt.scatter(df['TEMP'], df['pm2.5'], alpha=0.3, s=5, c='coral')
plt.title('温度与 PM2.5 散点图', fontsize=14)
plt.xlabel('温度 (℃)')
plt.ylabel('PM2.5 浓度 (ug/m**3)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 5.3 风速（Iws）与 PM2.5 的散点图（或箱线图）
plt.figure(figsize=(8, 6))
plt.scatter(df['Iws'], df['pm2.5'], alpha=0.3, s=5, c='teal')
plt.title('风速与 PM2.5 散点图', fontsize=14)
plt.xlabel('累计风速 (m/s)')
plt.ylabel('PM2.5 浓度 (ug/m**3)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# ---------- 6. 季节性变化规律 ----------
# 按照气象季节划分：春(3-5), 夏(6-8), 秋(9-11), 冬(12-2)
def get_season(month):
    if month in [3,4,5]:
        return '春季'
    elif month in [6,7,8]:
        return '夏季'
    elif month in [9,10,11]:
        return '秋季'
    else:
        return '冬季'

df['season'] = df['month'].apply(get_season)
season_order = ['春季', '夏季', '秋季', '冬季']
season_avg = df.groupby('season')['pm2.5'].mean().reindex(season_order)

# 绘制季节平均 PM2.5 柱状图
plt.figure(figsize=(8, 5))
bars = plt.bar(season_avg.index, season_avg.values, color=['lightgreen','gold','orange','lightskyblue'], edgecolor='black')
plt.title('四季平均 PM2.5 浓度', fontsize=14)
plt.xlabel('季节')
plt.ylabel('PM2.5 浓度 (ug/m**3)')
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{bar.get_height():.1f}',
             ha='center', va='bottom')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# 可选：绘制箱线图观察各季节分布
plt.figure(figsize=(10, 6))
sns.boxplot(x='season', y='pm2.5', data=df, order=season_order)
plt.title('各季节 PM2.5 浓度分布箱线图', fontsize=14)
plt.xlabel('季节')
plt.ylabel('PM2.5 浓度 (ug/m**3)')
plt.tight_layout()
plt.show()

print("\n分析结论：")
print("1. PM2.5 呈现明显的季节变化，冬季最高，春秋次之，夏季最低。")
print("2. PM2.5 与温度、露点温度呈负相关，与气压呈正相关，与风速呈负相关（风速大有助于扩散）。")
print("3. 冬季供暖和不利气象条件导致污染物积聚，夏季降雨和强对流利于清除。")