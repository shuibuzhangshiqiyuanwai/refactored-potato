# 课程资料整理器

自动将混杂的课程文件按类别（课件、代码、数据、文档、图片、作业等）整理到不同子目录，并生成整理报告。

## 快速开始

1. 将待整理的文件放入 `sample_materials` 目录（或任意目录）。
2. 预览整理计划（不实际执行）：
   ```bash
   python main.py --source sample_materials --target organized_materials --dry-run