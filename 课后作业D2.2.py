# 生成正态分布随机数 (均值=0, 标准差=1)
import numpy as np
import matplotlib.pyplot as plt
data = np.random.normal(loc=0, scale=1, size=1000)

# 统计分析
print("均值:", np.mean(data))
print("标准差:", np.std(data))
print("方差:", np.var(data))
print("中位数:", np.median(data))
print("最大值/最小值:", np.max(data), np.min(data))
print("25/75 百分位数:", np.percentile(data, [25, 75]))

np.random.seed(42)   # 可重复结果

# 参数设置
days = 252           # 一个交易年度
S0 = 100             # 初始价格
mu = 0.07            # 年化预期收益率
sigma = 0.2          # 年化波动率
dt = 1/days          # 时间步长

# 生成对数收益率并累积得到价格
returns = np.random.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), days)
price_series = S0 * np.exp(np.cumsum(returns))   # 累积乘积 -> 股价序列
print("模拟股价前5天:", price_series[:5])

# 日简单收益率
daily_returns = np.diff(price_series) / price_series[:-1]

# 年化收益率
annual_return = np.mean(daily_returns) * days
# 年化波动率
annual_volatility = np.std(daily_returns, ddof=1) * np.sqrt(days)

print(f"年化收益率: {annual_return:.4f} ({annual_return*100:.2f}%)")
print(f"年化波动率: {annual_volatility:.4f} ({annual_volatility*100:.2f}%)")

def moving_average(data, window):
    """用卷积实现简单移动平均"""
    return np.convolve(data, np.ones(window)/window, mode='valid')

ma_20 = moving_average(price_series, window=20)
ma_60 = moving_average(price_series, window=60)

print("20日均线前5个值:", ma_20[:5])
print("60日均线前5个值:", ma_60[:5])

# 生成第二支股票，与第一支有一定相关性
np.random.seed(123)
returns2_base = np.random.normal((0.08 - 0.5*0.25**2)*dt, 0.25*np.sqrt(dt), days)
# 引入相关性：混合部分第一支股票的收益率
rho = 0.6   # 目标相关系数
returns2 = rho * returns + np.sqrt(1 - rho**2) * returns2_base
price2 = 100 * np.exp(np.cumsum(returns2))

daily_ret2 = np.diff(price2) / price2[:-1]

# 协方差矩阵
cov_matrix = np.cov(daily_returns, daily_ret2)
print("日收益率协方差矩阵:\n", cov_matrix)
print("年化协方差矩阵:\n", cov_matrix * days)

# 组合方差 (等权重 50:50)
weights = np.array([0.5, 0.5])
port_variance = weights.T @ cov_matrix @ weights
port_volatility = np.sqrt(port_variance) * np.sqrt(days)
print(f"等权重组合年化波动率: {port_volatility:.4f} ({port_volatility*100:.2f}%)")

# 组合年化收益率
port_return = np.dot(weights, [np.mean(daily_returns), np.mean(daily_ret2)]) * days
print(f"等权重组合年化收益率: {port_return:.4f} ({port_return*100:.2f}%)")



plt.style.use('seaborn-v0_8-darkgrid')
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# 图1：股价走势与移动平均线
ax1 = axes[0]
ax1.plot(price_series, label='Stock 1', alpha=0.8)
ax1.plot(price2, label='Stock 2', alpha=0.8)
ax1.plot(range(19, days), ma_20, label='Stock1 20-day MA', linewidth=2)
ax1.plot(range(59, days), ma_60, label='Stock1 60-day MA', linewidth=2)
ax1.set_title('Simulated Stock Prices with Moving Averages')
ax1.legend()
ax1.set_ylabel('Price')

# 图2：日收益率分布
ax2 = axes[1]
ax2.hist(daily_returns, bins=50, alpha=0.6, label='Stock1 Returns', density=True)
ax2.hist(daily_ret2, bins=50, alpha=0.6, label='Stock2 Returns', density=True)
ax2.axvline(0, color='black', linestyle='--', linewidth=0.8)
ax2.set_title('Daily Returns Distribution')
ax2.legend()

# 图3：累积收益率
ax3 = axes[2]
cum_ret1 = price_series / price_series[0] - 1
cum_ret2 = price2 / price2[0] - 1
ax3.plot(cum_ret1, label='Stock1 Cumulative Return')
ax3.plot(cum_ret2, label='Stock2 Cumulative Return')
ax3.set_title('Cumulative Returns')
ax3.legend()
ax3.set_xlabel('Days')

plt.tight_layout()
plt.show()