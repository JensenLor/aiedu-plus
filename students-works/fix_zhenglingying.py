#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复并添加郑凌颖同学
"""

import csv
import os

def add_student():
    # 读取现有CSV文件
    csv_file = "学生基本信息.csv"
    
    # 先读取现有数据
    existing_data = []
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header = next(reader)  # 读取表头
            existing_data = list(reader)
    except Exception as e:
        print(f"读取文件出错: {e}")
        # 如果读取失败，创建新文件
        header = ['学号', '姓名', '年级', '擅长标签', '分类', '个人简介', '加入日期', '头像文件名']
        existing_data = []
    
    # 添加新学生
    new_student = [
        'zly004',  # 学号
        '郑凌颖',  # 姓名
        '小学三年级',  # 年级
        'Scratch,3D建模,Arduino,硬件编程,主板焊接',  # 擅长标签
        'hardware,3d,robot',  # 分类
        '三年级学生，学习Scratch、3D建模、巡线机器人、Arduino开源硬件编程和主板焊接，对硬件和编程有浓厚兴趣',  # 个人简介
        '2025-01-10',  # 加入日期
        'default_avatar.jpg'  # 头像文件名
    ]
    
    existing_data.append(new_student)
    
    # 写回文件
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(existing_data)
    
    print("✅ CSV文件已更新！")
    print(f"添加学生: {new_student[1]} (学号: {new_student[0]})")
    
    return new_student

def create_student_folder():
    """创建学生文件夹"""
    folder_name = "zly004_郑凌颖"
    folder_path = os.path.join("students", folder_name)
    
    os.makedirs(folder_path, exist_ok=True)
    
    print(f"✅ 创建文件夹: {folder_path}")
    return folder_path

if __name__ == "__main__":
    print("正在添加郑凌颖同学...")
    print("=" * 50)
    
    # 1. 添加到CSV文件
    student_info = add_student()
    
    # 2. 创建文件夹
    folder_path = create_student_folder()
    
    print("\n" + "=" * 50)
    print("✅ 添加完成！")
    print(f"\n学生信息:")
    print(f"  学号: {student_info[0]}")
    print(f"  姓名: {student_info[1]}")
    print(f"  年级: {student_info[2]}")
    print(f"  擅长: {student_info[3]}")
    print(f"  分类: {student_info[4]}")
    print(f"  加入日期: {student_info[6]}")
    print(f"  文件夹: {folder_path}")
    
    print("\n下一步:")
    print("  1. 运行 scripts/simple_update_data.py 更新JSON数据")
    print("  2. 运行 create_zip.bat 更新所有数据")
    print("  3. 启动网站服务器查看效果")