#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加学生：郑凌颖
"""

import csv
import os
from datetime import datetime

def add_student_manually():
    """手动添加郑凌颖同学"""
    
    # 读取现有学生数据
    csv_file = "学生基本信息.csv"
    students = []
    
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            students = list(reader)
    
    # 生成新学号
    existing_ids = [s.get('学号', '') for s in students if s.get('学号', '').startswith('stu')]
    if existing_ids:
        # 提取数字部分
        numbers = []
        for sid in existing_ids:
            if sid.startswith('stu'):
                try:
                    num = int(sid[3:])
                    numbers.append(num)
                except:
                    pass
        
        if numbers:
            next_num = max(numbers) + 1
        else:
            next_num = 1
    else:
        next_num = 1
    
    new_id = f"stu{next_num:03d}"
    
    # 创建新学生记录
    new_student = {
        '学号': new_id,
        '姓名': '郑凌颖',
        '年级': '小学三年级',
        '擅长标签': 'Scratch,3D建模,Arduino,硬件编程,主板焊接',
        '分类': 'hardware,3d',
        '个人简介': '三年级学生，学习Scratch、3D建模、巡线机器人、Arduino开源硬件编程和主板焊接，对硬件和编程有浓厚兴趣。',
        '加入日期': '2025-01-10',
        '头像文件名': 'default_avatar.jpg'
    }
    
    # 添加到学生列表
    students.append(new_student)
    
    # 写回CSV文件
    fieldnames = ['学号', '姓名', '年级', '擅长标签', '分类', '个人简介', '加入日期', '头像文件名']
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    
    print(f"✅ 学生添加成功！")
    print(f"   学号: {new_id}")
    print(f"   姓名: 郑凌颖")
    print(f"   年级: 小学三年级")
    print(f"   擅长: Scratch,3D建模,Arduino,硬件编程,主板焊接")
    print(f"   分类: hardware,3d")
    print(f"   加入日期: 2025-01-10")
    print(f"   个人简介: 三年级学生，学习Scratch、3D建模、巡线机器人、Arduino开源硬件编程和主板焊接")
    
    # 创建学生文件夹
    student_dir = f"students/{new_id}"
    os.makedirs(student_dir, exist_ok=True)
    print(f"   已创建文件夹: {student_dir}")
    
    return new_student

def update_json_data():
    """更新JSON数据"""
    try:
        # 导入simple_update_data模块
        import sys
        sys.path.append('.')
        
        # 创建简化版的更新函数
        import json
        import glob
        from datetime import datetime
        
        def calculate_study_months(join_date_str):
            """计算学习时长（月）"""
            try:
                join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
                current_date = datetime.now()
                months = (current_date.year - join_date.year) * 12 + (current_date.month - join_date.month)
                if current_date.day < join_date.day:
                    months -= 1
                return max(0, months)
            except:
                return 0
        
        # 读取学生数据
        students_data = []
        with open("学生基本信息.csv", 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 计算学习时长
                join_date = row.get('加入日期', '').strip()
                study_months = calculate_study_months(join_date)
                
                # 统计作品数量
                student_id = row.get('学号', '')
                works_dir = f"students/{student_id}"
                works_count = 0
                if os.path.exists(works_dir):
                    # 统计子目录数量（每个作品一个目录）
                    works_count = len([d for d in os.listdir(works_dir) 
                                      if os.path.isdir(os.path.join(works_dir, d)) and d.startswith('work')])
                
                # 构建学生JSON
                student_json = {
                    'id': student_id,
                    'name': row.get('姓名', ''),
                    'grade': row.get('年级', ''),
                    'tags': row.get('擅长标签', '').split(',') if row.get('擅长标签') else [],
                    'category': row.get('分类', '').split(',') if row.get('分类') else [],
                    'bio': row.get('个人简介', ''),
                    'joinDate': join_date,
                    'avatar': row.get('头像文件名', 'default_avatar.jpg'),
                    'studyMonths': study_months,
                    'worksCount': works_count
                }
                students_data.append(student_json)
        
        # 写入JSON文件
        output_dir = "generated"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "students.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(students_data, f, ensure_ascii=False, indent=2)
        
        print(f"📊 JSON数据已更新: {output_file}")
        print(f"   当前学生总数: {len(students_data)}")
        
        # 显示新添加的学生
        new_student = students_data[-1]
        print(f"\n🎯 新学生详情:")
        print(f"   学号: {new_student['id']}")
        print(f"   学习时长: {new_student['studyMonths']}个月")
        print(f"   作品数量: {new_student['worksCount']}个")
        
    except Exception as e:
        print(f"⚠️  JSON更新失败: {e}")

if __name__ == "__main__":
    print("正在添加学生：郑凌颖...")
    print("=" * 50)
    
    # 添加学生
    student = add_student_manually()
    
    print("\n" + "=" * 50)
    
    # 更新JSON数据
    update_json_data()
    
    print("\n" + "=" * 50)
    print("✅ 添加完成！")
    print("\n下一步：")
    print("  1. 运行 create_zip.bat 更新所有数据")
    print("  2. 启动网站服务器查看效果")
    print("  3. 网站将自动显示新学生")