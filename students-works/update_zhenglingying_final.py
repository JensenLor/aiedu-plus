#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终更新郑凌颖同学 - 尝试写入已打开的文件
"""

import csv
import os
import sys

def try_update_student_csv():
    """尝试更新学生基本信息.csv"""
    csv_file = "学生基本信息.csv"
    
    print(f"尝试更新文件: {csv_file}")
    
    try:
        # 尝试以读写模式打开文件
        with open(csv_file, 'r+', newline='', encoding='utf-8-sig') as f:
            # 读取现有数据
            reader = csv.reader(f)
            rows = list(reader)
            
            if not rows:
                print("文件为空，创建新文件")
                rows = [['学号', '姓名', '年级', '擅长标签', '分类', '个人简介', '加入日期', '头像文件名']]
            
            # 检查是否已存在郑凌颖
            student_exists = False
            for row in rows:
                if len(row) > 1 and row[1] == '郑凌颖':
                    student_exists = True
                    print("郑凌颖已存在，更新信息")
                    # 更新现有行
                    row[0] = 'zly004'  # 学号
                    row[1] = '郑凌颖'  # 姓名
                    row[2] = '小学三年级'  # 年级
                    row[3] = 'Scratch,3D建模,Arduino,硬件编程,主板焊接'  # 擅长标签
                    row[4] = 'hardware,3d,robot'  # 分类
                    row[5] = '三年级学生，学习Scratch、3D建模、巡线机器人、Arduino开源硬件编程和主板焊接，对硬件和编程有浓厚兴趣'  # 个人简介
                    row[6] = '2025-01-10'  # 加入日期
                    row[7] = 'default_avatar.jpg'  # 头像文件名
                    break
            
            if not student_exists:
                # 添加新学生
                new_row = [
                    'zly004',  # 学号
                    '郑凌颖',  # 姓名
                    '小学三年级',  # 年级
                    'Scratch,3D建模,Arduino,硬件编程,主板焊接',  # 擅长标签
                    'hardware,3d,robot',  # 分类
                    '三年级学生，学习Scratch、3D建模、巡线机器人、Arduino开源硬件编程和主板焊接，对硬件和编程有浓厚兴趣',  # 个人简介
                    '2025-01-10',  # 加入日期
                    'default_avatar.jpg'  # 头像文件名
                ]
                rows.append(new_row)
                print("添加新学生: 郑凌颖")
            
            # 写回文件
            f.seek(0)  # 回到文件开头
            f.truncate()  # 清空文件
            writer = csv.writer(f)
            writer.writerows(rows)
            
            print(f"[成功] 文件更新成功！")
            return True
            
    except PermissionError:
        print("[错误] 文件被其他程序占用，无法写入")
        print("请关闭Excel或其他正在使用此文件的程序")
        return False
    except Exception as e:
        print(f"[错误] 更新失败: {e}")
        return False

def create_student_folder():
    """创建学生文件夹"""
    folder_name = "zly004_郑凌颖"
    folder_path = os.path.join("students", folder_name)
    
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"[成功] 文件夹已创建/存在: {folder_path}")
        return True
    except Exception as e:
        print(f"[错误] 创建文件夹失败: {e}")
        return False

def run_data_update():
    """运行数据更新脚本"""
    try:
        print("\n运行数据更新脚本...")
        import subprocess
        result = subprocess.run(
            [sys.executable, "scripts/simple_update_data.py"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        print("输出:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"[错误] 运行更新脚本失败: {e}")
        return False

def main():
    print("=" * 60)
    print("郑凌颖同学信息更新系统")
    print("=" * 60)
    
    # 1. 尝试更新CSV文件
    print("\n[步骤1] 更新学生基本信息.csv")
    if not try_update_student_csv():
        print("\n⚠️  请先关闭Excel或其他打开此文件的程序")
        print("然后重新运行此脚本")
        return
    
    # 2. 创建文件夹
    print("\n[步骤2] 创建学生文件夹")
    create_student_folder()
    
    # 3. 运行数据更新
    print("\n[步骤3] 更新JSON数据")
    if run_data_update():
        print("\n[成功] 所有更新完成！")
        print("\n郑凌颖同学信息:")
        print("  学号: zly004")
        print("  姓名: 郑凌颖")
        print("  年级: 小学三年级")
        print("  擅长: Scratch,3D建模,Arduino,硬件编程,主板焊接")
        print("  分类: hardware,3d,robot")
        print("  加入日期: 2025-01-10")
        print("  学习时长: 15个月 (自动计算)")
    else:
        print("\n⚠️  数据更新可能有部分问题")
        print("请手动运行: python scripts/simple_update_data.py")
    
    print("\n" + "=" * 60)
    print("完成！")

if __name__ == "__main__":
    main()