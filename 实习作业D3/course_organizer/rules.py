"""
分类规则模块：定义后缀到目录的映射，以及作业关键词。
"""

# 后缀名 -> 目标子目录（统一使用小写后缀）
EXTENSION_MAP = {
    # 课件
    '.ppt': 'slides',
    '.pptx': 'slides',
    '.key': 'slides',
    # 代码
    '.py': 'code',
    '.ipynb': 'code',
    '.c': 'code',
    '.cpp': 'code',
    '.java': 'code',
    # 数据
    '.csv': 'data',
    '.xlsx': 'data',
    '.json': 'data',
    # 文档
    '.pdf': 'documents',
    '.doc': 'documents',
    '.docx': 'documents',
    '.txt': 'documents',
    '.md': 'documents',
    # 图片
    '.png': 'images',
    '.jpg': 'images',
    '.jpeg': 'images',
    '.gif': 'images',
}

# 文件名中包含这些关键词的，优先归入 homework
HOMEWORK_KEYWORDS = ['作业', '练习', '实验', '任务']