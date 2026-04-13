#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试智能表格系统
"""

import csv
import re
from datetime import datetime

def test_parsing():
    print("=== 智能表格系统解析测试 ===")
    print("=" * 50)
    
    # 测试学生解析
    print("\n[学生信息解析测试]")
    
    test_students = [
        "新增学生：张三，初中二年级，擅长Python和Web开发，喜欢AI项目，2026年4月7日加入",
        "学生：李四，小学五年级，Scratch很厉害，爱做游戏",
        "添加学生：王五，高中一年级，硬件达人，机器人比赛获奖"
    ]
    
    for text in test_students:
        print(f"\n输入: {text}")
        
        info = {}
        
        # 提取姓名
        match = re.search(r'新增学生[：:]\s*([^，,]+)', text) or \
                re.search(r'学生[：:]\s*([^，,]+)', text) or \
                re.search(r'添加学生[：:]\s*([^，,]+)', text)
        if match:
            info['姓名'] = match.group(1).strip()
            print(f"  提取姓名: {info['姓名']}")
        
        # 提取年级
        for grade in ['小学一年级', '小学二年级', '小学三年级', '小学四年级', '小学五年级', '小学六年级',
                     '初中一年级', '初中二年级', '初中三年级', '高中一年级', '高中二年级', '高中三年级']:
            if grade in text:
                info['年级'] = grade
                print(f"  提取年级: {info['年级']}")
                break
        
        # 提取技能
        skills = []
        if 'Python' in text:
            skills.append('Python')
        if 'Web' in text or '网页' in text:
            skills.append('Web开发')
        if 'Scratch' in text:
            skills.append('Scratch')
        if '硬件' in text or '机器人' in text:
            skills.append('硬件')
        if 'AI' in text or '人工智能' in text:
            skills.append('AI应用')
        
        if skills:
            info['擅长标签'] = ','.join(skills)
            print(f"  提取技能: {info['擅长标签']}")
        
        # 提取日期
        date_match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', text)
        if date_match:
            year, month, day = date_match.groups()
            info['加入日期'] = f"{year}-{int(month):02d}-{int(day):02d}"
            print(f"  提取日期: {info['加入日期']}")
        else:
            info['加入日期'] = datetime.now().strftime('%Y-%m-%d')
            print(f"  使用默认日期: {info['加入日期']}")
        
        print("  [解析完成]")
    
    # 测试作品解析
    print("\n[作品信息解析测试]")
    
    test_works = [
        '新增作品：学生zzy001，作品名"AI绘画助手"，用Python和深度学习，描述：基于Stable Diffusion的绘画工具',
        '作品：学生stu004，作品"智能家居控制"，Arduino+Python，难度中等'
    ]
    
    for text in test_works:
        print(f"\n输入: {text}")
        
        info = {}
        
        # 提取学生学号
        sid_match = re.search(r'学生(\w+)', text)
        if sid_match:
            info['学生学号'] = sid_match.group(1)
            print(f"  提取学号: {info['学生学号']}")
        
        # 提取作品名称
        name_match = re.search(r'作品名[：:\'"]?([^\'"，,]+)', text) or \
                     re.search(r'作品[：:\'"]?([^\'"，,]+)', text)
        if name_match:
            info['作品名称'] = name_match.group(1).strip()
            print(f"  提取作品名: {info['作品名称']}")
        
        # 提取技术标签
        tech_tags = []
        if 'Python' in text:
            tech_tags.append('Python')
        if '深度学习' in text or 'AI' in text:
            tech_tags.append('深度学习')
        if 'Arduino' in text:
            tech_tags.append('Arduino')
        if 'Stable Diffusion' in text:
            tech_tags.append('Stable Diffusion')
        
        if tech_tags:
            info['技术标签'] = ','.join(tech_tags)
            print(f"  提取技术: {info['技术标签']}")
        
        # 提取描述
        desc_match = re.search(r'描述[：:]\s*([^。]+)', text)
        if desc_match:
            info['作品描述'] = desc_match.group(1).strip()
            print(f"  提取描述: {info['作品描述'][:50]}...")
        
        # 提取难度
        if '简单' in text or '初级' in text:
            info['难度等级'] = '简单'
        elif '困难' in text or '高级' in text:
            info['难度等级'] = '困难'
        else:
            info['难度等级'] = '中等'
        
        print(f"  提取难度: {info['难度等级']}")
        print("  [解析完成]")
    
    # 检查当前数据
    print("\n[当前数据状态]")
    
    try:
        with open('学生基本信息.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            students = list(reader)
            print(f"  现有学生数量: {len(students)}")
            if students:
                print("  最后3名学生:")
                for student in students[-3:]:
                    print(f"    - {student.get('学号', '')}: {student.get('姓名', '')}")
    except FileNotFoundError:
        print("  学生基本信息.csv 未找到")
    
    try:
        with open('作品信息.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            works = list(reader)
            print(f"  现有作品数量: {len(works)}")
    except FileNotFoundError:
        print("  作品信息.csv 未找到")
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n使用说明:")
    print("  1. 直接发文字给我，我会帮你更新表格")
    print("  2. 格式示例:")
    print("     新增学生：姓名，年级，擅长...")
    print("     新增作品：学生学号，作品名...")

if __name__ == "__main__":
    test_parsing()