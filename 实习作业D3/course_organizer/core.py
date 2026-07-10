"""
核心整理模块：扫描文件、生成整理计划、执行复制/移动、生成报告。
"""

import shutil
from pathlib import Path
from collections import defaultdict
from course_organizer.rules import EXTENSION_MAP, HOMEWORK_KEYWORDS

def classify_file(filename: str) -> str:
    """
    根据文件名和扩展名返回分类子目录名称。
    规则：先检查作业关键词，再按后缀匹配，否则归入 'others'。
    """
    # 检查作业关键词
    for kw in HOMEWORK_KEYWORDS:
        if kw in filename:
            return 'homework'
    # 获取后缀（小写）
    suffix = Path(filename).suffix.lower()
    return EXTENSION_MAP.get(suffix, 'others')

def generate_plan(source_dir: Path) -> list[tuple[Path, Path, str]]:
    """
    扫描源目录，生成整理计划。
    返回列表，每个元素为 (源文件路径, 目标文件路径, 分类目录名)。
    """
    plan = []
    if not source_dir.exists():
        raise FileNotFoundError(f"源目录不存在: {source_dir}")
    for file_path in source_dir.iterdir():
        if file_path.is_file():
            category = classify_file(file_path.name)
            # 目标路径暂时记为 target_root / category / filename（最终解决重名时调整）
            target_path = Path(category) / file_path.name
            plan.append((file_path, target_path, category))
    return plan

def resolve_target(target_base: Path, relative_target: Path) -> Path:
    """
    解决目标路径重名问题：若文件已存在，则在主文件名后添加 _1, _2...。
    返回最终可用的目标路径（不实际创建文件）。
    """
    target_dir = target_base / relative_target.parent
    stem = relative_target.stem
    suffix = relative_target.suffix
    candidate = target_dir / f"{stem}{suffix}"
    counter = 1
    while candidate.exists():
        candidate = target_dir / f"{stem}_{counter}{suffix}"
        counter += 1
    return candidate

def execute_plan(plan, target_base: Path, *, mode='copy', dry_run=False):
    """
    根据整理计划执行操作。
    - mode: 'copy' 或 'move'
    - dry_run: True 时只打印计划，不实际操作也不创建目录
    返回一个列表，记录每个文件最终从哪到哪，以及分类。
    """
    if dry_run:
        print("【DRY RUN 模式】以下是将要执行的操作（不会实际修改文件系统）:\\n")
        for src, rel_target, category in plan:
            final_target = target_base / rel_target
            print(f"  [{category}] {src.name} -> {final_target}")
        print("\\n提示：去掉 --dry-run 参数即可真正整理。")
        return []

    # 实际执行
    records = []
    for src, rel_target, category in plan:
        # 创建分类子目录
        final_target_dir = target_base / rel_target.parent
        final_target_dir.mkdir(parents=True, exist_ok=True)

        # 解决重名，得到实际使用的目标路径
        final_target = resolve_target(target_base, rel_target)

        # 复制或移动
        if mode == 'copy':
            shutil.copy2(src, final_target)  # copy2 保留元数据
        elif mode == 'move':
            shutil.move(src, final_target)
        else:
            raise ValueError(f"不支持的模式: {mode}")

        records.append({
            'source': src,
            'target': final_target,
            'category': category
        })
    return records

def generate_report(records, target_base: Path, mode: str):
    """
    在目标根目录生成 整理报告.txt。
    records: execute_plan 返回的记录列表。
    """
    report_path = target_base / '整理报告.txt'
    category_count = defaultdict(int)
    lines = []
    lines.append(f"整理模式: {'移动' if mode == 'move' else '复制'}")
    lines.append(f"整理文件总数: {len(records)}")
    lines.append("=" * 40)
    for rec in records:
        cat = rec['category']
        category_count[cat] += 1
        lines.append(f"[{cat}] {rec['source'].name} -> {rec['target'].relative_to(target_base)}")
    lines.append("=" * 40)
    lines.append("各类文件数量统计:")
    for cat, count in sorted(category_count.items()):
        lines.append(f"  {cat}: {count} 个")
    report_content = "\\n".join(lines)
    report_path.write_text(report_content, encoding='utf-8')
    print(f"整理报告已生成: {report_path}")