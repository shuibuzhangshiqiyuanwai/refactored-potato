import pandas as pd
import numpy as np

# ==================== 1. 读取数据 ====================
df = pd.read_csv('train.csv')
print("====== 原始数据概览 ======")
print(f"行列数: {df.shape}")
print(df.info())
print("\\n缺失值统计:")
print(df.isnull().sum())
print(f"\\n完全重复的行数: {df.duplicated().sum()}")

# ==================== 2. 缺失值处理 ====================
# 2.1 Age（年龄）：用中位数填充
age_median = df['Age'].median()
df['Age'] = df['Age'].fillna(age_median)          # 推荐写法

# 2.2 Embarked（登船港口）：用众数填充
embarked_mode = df['Embarked'].mode()[0]
df['Embarked'] = df['Embarked'].fillna(embarked_mode)

# 2.3 Cabin（客舱号）：转换为缺失标记
df['Cabin_missing'] = df['Cabin'].isnull().astype(int)
df.drop('Cabin', axis=1, inplace=True)

# 2.4 Fare（票价）：异常值处理（如果存在）
if df['Fare'].isnull().any():
    df['Fare'] = df['Fare'].fillna(df['Fare'].median())
df.loc[df['Fare'] <= 0, 'Fare'] = df['Fare'].median()

print("\\n====== 缺失值处理后 ======")
print(df.isnull().sum())

# ==================== 3. 重复记录处理 ====================
# 检查完全重复的行（所有列值相同）
dup_count = df.duplicated().sum()
if dup_count > 0:
    print(f"发现 {dup_count} 条重复记录，已删除。")
    df.drop_duplicates(inplace=True)
else:
    print("无完全重复的行。")

# 可进一步考虑基于关键列（如 Name + Ticket）的业务重复，
# 此处仅演示删除完全重复行。

# ==================== 4. 数据类型转换与格式标准化 ====================
# 4.1 类型转换
df['Survived'] = df['Survived'].astype('category')
df['Pclass'] = df['Pclass'].astype('category')
df['Sex'] = df['Sex'].astype('category')
df['Embarked'] = df['Embarked'].astype('category')
# Age 和 Fare 保持为 float

# 4.2 文本字段标准化
# 处理 Name：统一大小写，去除多余空格
df['Name'] = df['Name'].str.strip().str.title()
# 处理 Ticket 字段：转为字符串，统一大小写
df['Ticket'] = df['Ticket'].astype(str).str.strip().str.upper()

# 4.3 从 Name 中提取称谓（Title），可作为新特征
df['Title'] = df['Name'].str.extract(r',\\s*(\\w+\\.)')[0]   # 提取如 Mr.
df['Title'] = df['Title'].str.replace('.', '', regex=False)
# 归类稀少称谓
rare_titles = ['Lady', 'Sir', 'Countess', 'Jonkheer', 'Don', 'Dona']
df.loc[df['Title'].isin(rare_titles), 'Title'] = 'Noble'
# 将 Mlle 和 Ms 归入 Miss
df.loc[df['Title'].isin(['Mlle', 'Ms']), 'Title'] = 'Miss'
df.loc[df['Title'] == 'Mme', 'Title'] = 'Mrs'
df['Title'] = df['Title'].astype('category')

# 4.4 离散化 Age（可选，便于分析）
age_bins = [0, 12, 18, 35, 60, 100]
age_labels = ['Child', 'Teenager', 'YoungAdult', 'MiddleAge', 'Senior']
df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
df['AgeGroup'] = df['AgeGroup'].astype('category')

# 4.5 家庭规模特征（SibSp + Parch + 本人）
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

print("数据类型转换后")
print(df.dtypes)
print("清洗后数据前5行 ")
print(df.head())

# 保存清洗后的数据
df.to_csv('titanic_cleaned.csv', index=False)
print("\n清洗完成，已保存为 'titanic_cleaned.csv'。")