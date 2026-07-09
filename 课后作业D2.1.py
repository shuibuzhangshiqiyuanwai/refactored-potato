import numpy as np

# 1D 数组
arr_1d = np.array([1, 2, 3, 4, 5])
print("1D 数组:\n", arr_1d, "\n")

# 2D 数组 (矩阵)
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print("2D 数组:\n", arr_2d, "\n")

# 3D 数组
arr_3d = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]],
                   [[9, 10], [11, 12]]])
print("3D 数组形状:", arr_3d.shape)
print(arr_3d)

# 1D 切片
print("1D 前三个元素:", arr_1d[:3])
print("1D 每隔一个元素:", arr_1d[::2])

# 2D 索引与切片
print("2D 第0行:", arr_2d[0])
print("2D 第1列:", arr_2d[:, 1])
print("2D 前两行，后两列:\n", arr_2d[:2, 1:])

# 3D 切片
print("3D 第一个矩阵的第二行:", arr_3d[0, 1])     # [3,4]
print("3D 所有矩阵的第0列:\n", arr_3d[:, :, 0])

# reshape
reshaped = arr_2d.reshape(1, 9)   # 变为1x9
print("reshape 1x9:\n", reshaped)

# 展平
flat = arr_2d.flatten()           # 变为1D
print("展平后:", flat)

# 转置
transposed = arr_2d.T
print("2D 转置:\n", transposed)

# 增加维度
expanded = np.expand_dims(arr_1d, axis=0)  # (5,) -> (1,5)
print("增加维度后形状:", expanded.shape)

def matrix_operations(A, B):
    """实现加法、乘法（矩阵乘）、转置"""
    add = A + B                     # 逐元素加法
    try:
        mul = A @ B                 # 矩阵乘法
    except ValueError:
        mul = "无法相乘，维度不匹配"
    trans_A = A.T
    return add, mul, trans_A

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

add, mul, trans_A = matrix_operations(A, B)
print("A + B:\n", add)
print("A × B:\n", mul)
print("A 转置:\n", trans_A)