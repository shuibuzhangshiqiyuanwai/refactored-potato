import math
import os

HISTORY_FILE = "calc_history.txt"
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

def power(a, b):
    return a ** b

def sqrt_op(a):
    """开方运算，单参数"""
    if a < 0:
        raise ValueError("不能对负数开平方")
    return math.sqrt(a)

def save_history(expression, result):
    """将计算记录追加写入文件"""
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"{expression} = {result}\n")
    except IOError as e:
        print(f"保存历史记录失败: {e}")

def read_history():
    """从文件读取并显示历史记录"""
    if not os.path.exists(HISTORY_FILE):
        print("暂无历史记录文件。")
        return
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            print("历史记录为空。")
        else:
            print("===== 计算历史 =====")
            for line in lines:
                print(line.strip())
    except IOError as e:
        print(f"读取历史记录失败: {e}")

while True:
        print("1. 加法")
        print("2. 减法")
        print("3. 乘法")
        print("4. 除法")
        print("5. 幂运算")
        print("6. 开方")
        print("7. 查看历史记录")
        print("8. 退出")
        choice = input("请选择操作(1-8): ")

        if choice in ('1', '2', '3', '4', '5'):
            try:
                a = float(input("请输入第一个数: "))
                b = float(input("请输入第二个数: "))
            except ValueError:
                print("输入必须是数字。")
                continue

            if choice == '1':
                result = add(a, b)
                expr = f"{a} + {b}"
            elif choice == '2':
                result = subtract(a, b)
                expr = f"{a} - {b}"
            elif choice == '3':
                result = multiply(a, b)
                expr = f"{a} * {b}"
            elif choice == '4':
                try:
                    result = divide(a, b)
                    expr = f"{a} / {b}"
                except ValueError as e:
                    print(f"错误: {e}")
                    continue
            elif choice == '5':
                result = power(a, b)
                expr = f"{a} ^ {b}"

            print(f"结果: {result}")
            save_history(expr, result)

        elif choice == '6':
            try:
                a = float(input("请输入一个数: "))
                result = sqrt_op(a)
                expr = f"√{a}"
                print(f"结果: {result}")
                save_history(expr, result)
            except ValueError as e:
                print(f"错误: {e}")

        elif choice == '7':
            read_history()

        elif choice == '8':
            print("谢谢使用！")
            break
        else:
            print("无效选择，请重新输入。")

