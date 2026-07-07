students = {}  # {学号: {"姓名":..., "成绩":{科目:分数}}}
while True:
        print("1. 录入成绩")
        print("2. 查询成绩")
        print("3. 统计信息")
        print("4. 退出")
        choice = input("请选择功能(1-4): ")

        if choice == '1':
            stu_id = input("请输入学号: ")
            name = input("请输入姓名: ")
            scores = {}
            while True:
                subject = input("请输入科目名称(直接回车结束): ")
                if subject == "":
                    break
                try:
                    score = float(input(f"请输入{subject}成绩: "))
                    scores[subject] = score
                except ValueError:
                    print("成绩必须是数字，请重新输入该科目。")
                    continue
            students[stu_id] = {"姓名": name, "成绩": scores}
            print(f"学生 {name} 的成绩已录入。")

        elif choice == '2':
            stu_id = input("请输入要查询的学号: ")
            if stu_id in students:
                info = students[stu_id]
                print(f"姓名: {info['姓名']}")
                print("各科成绩:")
                for subj, scr in info['成绩'].items():
                    print(f"  {subj}: {scr}")
                if info['成绩']:
                    avg = sum(info['成绩'].values()) / len(info['成绩'])
                    print(f"平均分: {avg:.2f}")
                else:
                    print("暂无成绩记录。")
            else:
                print("未找到该学号对应的学生。")

        elif choice == '3':
            if not students:
                print("暂无学生数据。")
                continue

            # 用于总体统计的成绩列表
            all_scores = []

            subject_scores = {}

            # 遍历所有学生，收集成绩
            for stu_id, info in students.items():
                for subj, scr in info['成绩'].items():
                    all_scores.append(scr)
                    if subj not in subject_scores:
                        subject_scores[subj] = []
                    subject_scores[subj].append(scr)

            if not all_scores:
                print("没有任何成绩数据。")
                continue
            for subj, score_list in subject_scores.items():
                subj_avg = sum(score_list) / len(score_list)
                subj_max = max(score_list)
                subj_min = min(score_list)
                print(f"《{subj}》")
                print(f"  平均分: {subj_avg:.2f}")
                print(f"  最高分: {subj_max}")
                print(f"  最低分: {subj_min}")

        elif choice == '4':
            print("感谢使用，再见！")
            break
        else:
            print("输入无效，请输入1-4之间的数字。")



