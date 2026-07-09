import numpy as np

class ScoreAnalyzer:
    def __init__(self):
        self.names = []       # 学生姓名列表
        self.scores = []      # 学生成绩列表
        self.score_array = None  # 用于 NumPy 计算的数组

    # ---------- 功能1：输入成绩 ----------
    def input_scores(self):
        print("\n========== 输入成绩数据 ==========")
        try:
            n = int(input("请输入学生人数："))
            if n <= 0:
                print("学生人数必须大于0！")
                return
        except ValueError:
            print("输入无效，请输入整数！")
            return

        self.names = []
        self.scores = []
        for i in range(n):
            name = input(f"请输入第{i+1}个学生姓名：").strip()
            while True:
                try:
                    score = float(input("请输入成绩："))
                    if 0 <= score <= 100:
                        break
                    else:
                        print("成绩应在 0~100 之间，请重新输入。")
                except ValueError:
                    print("请输入有效的数字！")
            self.names.append(name)
            self.scores.append(score)

        self.score_array = np.array(self.scores)
        print("成绩录入完成！")

    # ---------- 功能2：成绩统计 ----------
    def show_statistics(self):
        if self.score_array is None:
            print("\n请先输入成绩数据！")
            return

        print("\n========== 成绩统计 ==========")
        print(f"平均分：{np.mean(self.score_array):.2f}")
        print(f"最高分：{np.max(self.score_array):.2f}")
        print(f"最低分：{np.min(self.score_array):.2f}")
        print(f"标准差：{np.std(self.score_array, ddof=0):.2f}")
        print(f"中位数：{np.median(self.score_array):.2f}")

    # ---------- 功能3：成绩排名 ----------
    def show_ranking(self):
        if self.score_array is None:
            print("\n请先输入成绩数据！")
            return

        print("\n========== 成绩排名（降序）==========")
        # 使用 argsort 获取排序索引，降序排列
        sorted_indices = np.argsort(self.score_array)[::-1]
        rank = 1
        for idx in sorted_indices:
            print(f"第{rank}名：{self.names[idx]} - {self.scores[idx]}分")
            rank += 1

    # ---------- 功能4：成绩分布 ----------
    def show_distribution(self):
        if self.score_array is None:
            print("\n请先输入成绩数据！")
            return

        #等级区间：A:90-100, B:80-89, C:70-79, D:60-69, E:0-59
        bins = [0, 60, 70, 80, 90, 101]   # 注意上限为101以包含100
        labels = ['E (0-59)', 'D (60-69)', 'C (70-79)', 'B (80-89)', 'A (90-100)']

        # 使用 np.histogram 或 digitize
        counts, _ = np.histogram(self.score_array, bins=bins)
        total = len(self.score_array)

        print("\n========== 成绩分布 ==========")
        for i, label in enumerate(labels):
            count = counts[i]
            percent = count / total * 100
            print(f"{label}: {count}人, 占比 {percent:.1f}%")

    # ---------- 功能5：查询学生成绩 ----------
    def query_score(self):
        if not self.names:
            print("\n请先输入成绩数据！")
            return

        name = input("\n请输入要查询的学生姓名：").strip()
        found = False
        for i, n in enumerate(self.names):
            if n == name:
                print(f"{name} 的成绩为：{self.scores[i]}分")
                found = True
                break
        if not found:
            print(f"未找到学生 {name}")

    # ---------- 主菜单 ----------
    def menu(self):
        while True:
            print("\n" + "="*30)
            print("     成绩分析系统")
            print("="*30)
            print("1. 输入成绩数据")
            print("2. 查看成绩统计")
            print("3. 查看成绩排名")
            print("4. 查看成绩分布")
            print("5. 查询学生成绩")
            print("6. 退出系统")
            choice = input("\n请选择：").strip()

            if choice == '1':
                self.input_scores()
            elif choice == '2':
                self.show_statistics()
            elif choice == '3':
                self.show_ranking()
            elif choice == '4':
                self.show_distribution()
            elif choice == '5':
                self.query_score()
            elif choice == '6':
                print("感谢使用！")
                break
            else:
                print("无效选择，请重新输入！")

if __name__ == '__main__':
    analyzer = ScoreAnalyzer()
    analyzer.menu()