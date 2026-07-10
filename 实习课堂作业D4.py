import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

orders = pd.DataFrame({
    'order_id': [f'O{number}' for number in range(1001, 1019)],
    'region': ['华东','华北','华南','华东','西南','华北','华南','华东','西南','华北','华东','华南','西南','华东','华北','华南','华东','西南'],
    'product': ['机械键盘','无线鼠标','显示器','扩展坞','机械键盘','显示器','无线鼠标','显示器','扩展坞','机械键盘','无线鼠标','扩展坞','显示器','机械键盘','扩展坞','显示器','无线鼠标','机械键盘'],
    'category': ['外设','外设','显示设备','配件','外设','显示设备','外设','显示设备','配件','外设','外设','配件','显示设备','外设','配件','显示设备','外设','外设'],
    'quantity': [2,3,1,4,5,2,6,1,3,2,8,2,1,3,5,2,4,6],
    'unit_price': [289,129,1299,399,289,1299,129,1299,399,289,129,399,1299,289,399,1299,129,289],
    'member_level': ['金卡','普通','银卡','金卡','银卡','普通','金卡','银卡','普通','金卡','银卡','金卡','普通','银卡','金卡','金卡','普通','银卡'],
    'coupon_rate': [0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.08,0.00,0.10],
    'salesperson': ['小林','小周','小陈','小林','小赵','小周','小陈','小林','小赵','小周','小林','小陈','小赵','小林','小周','小陈','小林','小赵']
})
# 1.1 数据规模与列名
print("## 任务 1：快速理解数据1. 输出数据的行数、列数和所有列名。2. 分别取出 `region` 单列，以及 `order_id`、`product`、`quantity` 三列，并打印二者类型。3. 使用 `iloc` 取第 4～8 行、前 4 列。4. 使用 `loc` 找出“华东”订单，仅展示 `order_id`、`product`、`member_level`。5. 回答：为什么长期维护的业务代码通常更推荐 `loc`？")
print("行数:", orders.shape[0], "列数:", orders.shape[1])
print("列名:", orders.columns.tolist())
# 解释：数据集共18行10列，列出全部字段名称。
region_series = orders['region']
subset_df = orders[['order_id', 'product', 'quantity']]
print(type(region_series))   # <class 'pandas.core.series.Series'>
print(type(subset_df))       # <class 'pandas.core.frame.DataFrame'>
print("# 解释：取单列得到Series，取多列得到DataFrame。")
print("# 1.3 iloc取第4～8行、前4列（索引3到7，列0到3）")
print(orders.iloc[3:8, :4])
# 解释：按位置切片，展示订单O1004~O1008的前四列。
print("# 1.4 loc找出“华东”订单指定列")
print(orders.loc[orders['region'] == '华东', ['order_id', 'product', 'member_level']])
# 解释：用布尔标签筛选华东地区记录，仅保留订单号、商品和会员等级。
print("5. 回答：为什么长期维护的业务代码通常更推荐 `loc`？")
print(" 回答：loc基于标签筛选，即使DataFrame索引发生变动（如增删行），标签仍然准确，# 可避免位置偏移导致的错误，代码可读性更高，更稳健。")

print("## 任务 2：构造订单结算指标")

analysis = orders.assign(
    gross_amount = orders['quantity'] * orders['unit_price'],
    member_discount = np.where(orders['member_level'] == '金卡', 0.10,
                        np.where(orders['member_level'] == '银卡', 0.05, 0.00)),
    payable_amount = lambda df: (df['gross_amount'] * (1 - df['member_discount']) * (1 - df['coupon_rate'])).round(2),
    shipping_fee = lambda df: np.where(df['payable_amount'] >= 1000, 0, 20),
    final_amount = lambda df: (df['payable_amount'] + df['shipping_fee']).round(2)
)

# 展示前8行相关字段
print(analysis[['order_id', 'gross_amount', 'member_discount', 'payable_amount', 'shipping_fee', 'final_amount']].head(8))
print("# 任务 3：复杂条件筛选")

# 分别定义3个布尔条件

cond1 = analysis['region'].isin(['华东', '华南'])
cond2 = analysis['final_amount'] >= 700
cond3 = (analysis['quantity'] >= 2) | (analysis['member_level'] == '金卡')

# 组合mask
mask = cond1 & cond2 & cond3
key_orders = analysis.loc[mask, ['order_id', 'region', 'product', 'quantity', 'member_level', 'final_amount']]
print(key_orders.sort_values('final_amount', ascending=False))
print("# 任务 4：封装可复用处理函数")
def add_order_level(df):
    level = np.where(df['final_amount'] >= 2000, '战略订单',
              np.where(df['final_amount'] >= 1000, '重点订单', '普通订单'))
    return df.assign(order_level=level)

leveled_orders = analysis.pipe(add_order_level)
print(leveled_orders['order_level'].value_counts())

print("函数使用嵌套 np.where 实现三档分级，通过 pipe 调用传入原表，返回新 DataFrame，不修改原表。")
print("任务 5：一条链完成经营汇总")
region_report = (analysis
                 .pipe(add_order_level)
                 .query('final_amount >= 500')
                 .groupby(['region', 'order_level'])
                 .agg(
                     order_count=('order_id', 'count'),
                     quantity_sum=('quantity', 'sum'),
                     revenue_sum=('final_amount', 'sum'),
                     revenue_mean=('final_amount', 'mean')
                 )
                 .sort_values('revenue_sum', ascending=False)
                 .round({'revenue_mean': 2})
                )
print(region_report)
#一条方法链完成数据增强、过滤、分组聚合与排序，未产生任何中间 DataFrame，直接输出区域×订单等级的经营汇总表。




print("任务 6：经营诊断与表达"
      )

# 成交金额最高的销售人员
sales_total = analysis.groupby('salesperson')['final_amount'].sum()
top_sales = sales_total.idxmax()
total_sales_amount = sales_total.max()

# 该销售人员在哪个地区成交额最高
top_person_data = analysis[analysis['salesperson'] == top_sales]
region_amount = top_person_data.groupby('region')['final_amount'].sum()
top_region = region_amount.idxmax()
top_region_amount = region_amount.max()

# 地区贡献率
contribution = top_region_amount / total_sales_amount

print(f"销售人员：{top_sales}")
print(f"核心地区：{top_region}")
print(f"总成交金额：{total_sales_amount:.2f}")
print(f"核心地区金额：{top_region_amount:.2f}")
print(f"地区贡献率：{contribution:.2%}")
print(f"{top_sales}整体成交额最高，其核心业绩来源为{top_region}，该地区贡献了其总成交额的{contribution:.2%}，应重点维护{top_region}区域客户关系，继续深耕。")