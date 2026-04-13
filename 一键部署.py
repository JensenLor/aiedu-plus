#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aiedu.plus 一键部署脚本
使用方式：
    python 一键部署.py [提交信息]
    python 一键部署.py              # 使用默认提交信息
    python 一键部署.py "修复bug"    # 自定义提交信息
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """执行命令并返回结果"""
    print(f"\n[{description}]")
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[OK] {description}成功")
        if result.stdout:
            print(result.stdout.strip())
        return True
    else:
        print(f"[错误] {description}失败!")
        if result.stderr:
            print(result.stderr.strip())
        return False

def main():
    print("=" * 40)
    print("   aiedu.plus 一键部署脚本")
    print("=" * 40)
    
    # 获取提交信息
    commit_msg = "更新 aiedu.plus"
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    else:
        print("\n请输入提交信息（直接回车使用默认值）:")
        user_input = input(f"提交信息 [{commit_msg}]: ").strip()
        if user_input:
            commit_msg = user_input
    
    # Step 1: git add
    if not run_command("git add -A", "添加文件到Git"):
        input("\n按回车键退出...")
        sys.exit(1)
    
    # Step 2: git commit
    commit_cmd = f'git commit -m "{commit_msg}"'
    if not run_command(commit_cmd, "提交更改"):
        print("提示: 可能没有文件需要提交")
        # 不退出，继续尝试推送
    
    # Step 3: git push
    if not run_command("git push origin master:main", "推送到GitHub"):
        input("\n按回车键退出...")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("   部署完成!")
    print("   约1-2分钟后 Vercel 自动部署生效")
    print("=" * 40)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
