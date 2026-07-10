"""
课程资料整理器 - 入口程序
用法示例：
  python main.py --source sample_materials --target organized_materials --dry-run
  python main.py --source sample_materials --target organized_materials
  python main.py --source sample_materials --target organized_materials --mode move
"""

import argparse
from pathlib import Path
from course_organizer.core import generate_plan, execute_plan, generate_report

def main():
    parser = argparse.ArgumentParser(description="课程资料自动整理工具")
    parser.add_argument('--source', required=True, help='原始资料目录')
    parser.add_argument('--target', required=True, help='目标整理目录')
    parser.add_argument('--dry-run', action='store_true', help='仅预览整理计划，不实际操作')
    parser.add_argument('--mode', choices=['copy', 'move'], default='copy',
                        help='整理模式：copy（复制，默认）或 move（移动）')
    args = parser.parse_args()

    source_dir = Path(args.source)
    target_dir = Path(args.target)

    # 1. 生成整理计划
    plan = generate_plan(source_dir)
    if not plan:
        print("源目录中没有文件需要整理。")
        return

    # 2. 执行计划（dry_run 模式下仅打印）
    records = execute_plan(plan, target_dir, mode=args.mode, dry_run=args.dry_run)

    # 3. 真实整理后生成报告
    if not args.dry_run and records:
        generate_report(records, target_dir, args.mode)

if __name__ == '__main__':
    main()
