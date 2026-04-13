#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能语音/文字转表格系统
直接输入语音转文字或纯文本，自动更新所有表格
"""

import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
import sys

# 路径配置
BASE_DIR = Path(__file__).parent
STUDENT_CSV = BASE_DIR / "学生基本信息.csv"
WORKS_CSV = BASE_DIR / "作品信息.csv"
SOCIAL_CSV = BASE_DIR / "社交数据.csv"
STUDENTS_DIR = BASE_DIR / "students"
GENERATED_DIR = BASE_DIR / "generated"
DOWNLOADS_DIR = BASE_DIR / "downloads"

def ensure_dirs():
    """确保必要的目录存在"""
    for dir_path in [STUDENTS_DIR, GENERATED_DIR, DOWNLOADS_DIR]:
        dir_path.mkdir(exist_ok=True)

def read_csv_as_dict(filepath):
    """读取CSV文件为字典列表"""
    if not filepath.exists():
        return []
    
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_dict_to_csv(filepath, data, fieldnames):
    """将字典列表写入CSV文件"""
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_next_student_id():
    """生成下一个学号"""
    students = read_csv_as_dict(STUDENT_CSV)
    if not students:
        return "stu001"
    
    # 提取所有学号并找到最大值
    student_ids = [s.get('学号', '') for s in students if s.get('学号', '').startswith('stu')]
    if not student_ids:
        return "stu001"
    
    # 提取数字部分
    numbers = []
    for sid in student_ids:
        match = re.search(r'stu(\d+)', sid)
        if match:
            numbers.append(int(match.group(1)))
    
    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 1
    
    return f"stu{next_num:03d}"

def generate_next_work_id():
    """生成下一个作品ID"""
    works = read_csv_as_dict(WORKS_CSV)
    if not works:
        return "work001"
    
    # 提取所有作品ID
    work_ids = [w.get('作品ID', '') for w in works if w.get('作品ID', '').startswith('work')]
    if not work_ids:
        return "work001"
    
    # 提取数字部分
    numbers = []
    for wid in work_ids:
        match = re.search(r'work(\d+)', wid)
        if match:
            numbers.append(int(match.group(1)))
    
    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 1
    
    return f"work{next_num:03d}"

def parse_student_text(text):
    """解析学生信息文本"""
    info = {
        '姓名': '',
        '年级': '',
        '擅长标签': '',
        '分类': '',
        '个人简介': '',
        '加入日期': datetime.now().strftime('%Y-%m-%d'),
        '头像文件名': 'default_avatar.jpg'
    }
    
    # 简单关键词匹配（实际应用可用更复杂的NLP）
    text_lower = text.lower()
    
    # 提取姓名（假设"新增学生："后的第一个词是姓名）
    match = re.search(r'新增学生[：:]\s*([^，,]+)', text)
    if match:
        info['姓名'] = match.group(1).strip()
    
    # 提取年级
    grade_patterns = [
        ('小学一年级', '一年级'), ('小学二年级', '二年级'), ('小学三年级', '三年级'),
        ('小学四年级', '四年级'), ('小学五年级', '五年级'), ('小学六年级', '六年级'),
        ('初中一年级', '初一'), ('初中二年级', '初二'), ('初中三年级', '初三'),
        ('高中一年级', '高一'), ('高中二年级', '高二'), ('高中三年级', '高三')
    ]
    
    for pattern, grade in grade_patterns:
        if pattern in text:
            info['年级'] = pattern
            break
    
    # 提取擅长标签
    skills = []
    if 'python' in text_lower or 'Python' in text:
        skills.append('Python')
    if 'html' in text_lower or 'HTML' in text:
        skills.append('HTML/CSS')
    if 'javascript' in text_lower or 'JavaScript' in text or 'js' in text_lower:
        skills.append('JavaScript')
    if 'ai' in text_lower or '人工智能' in text or '深度学习' in text:
        skills.append('AI应用')
    if 'arduino' in text_lower or '硬件' in text or '机器人' in text:
        skills.append('硬件')
    if 'scratch' in text_lower or 'Scratch' in text:
        skills.append('Scratch')
    if 'web' in text_lower or '网页' in text or '网站' in text:
        skills.append('Web开发')
    
    if skills:
        info['擅长标签'] = ','.join(skills)
    
    # 提取分类
    categories = []
    if any(skill in ['Python', 'AI应用', '深度学习'] for skill in skills):
        categories.append('ai')
    if any(skill in ['HTML/CSS', 'JavaScript', 'Web开发'] for skill in skills):
        categories.append('web')
    if '硬件' in skills or 'Arduino' in text_lower:
        categories.append('hardware')
    if 'Scratch' in skills or '游戏' in text:
        categories.append('game')
    
    if categories:
        info['分类'] = ','.join(categories)
    
    # 提取个人简介（尝试从描述中提取）
    desc_match = re.search(r'描述[：:]\s*([^。]+)', text)
    if desc_match:
        info['个人简介'] = desc_match.group(1).strip()
    elif '喜欢' in text or '热爱' in text or '兴趣' in text:
        # 尝试提取兴趣部分
        interest_match = re.search(r'喜欢([^，,。]+)', text)
        if interest_match:
            info['个人简介'] = f"喜欢{interest_match.group(1).strip()}的学生"
    
    # 提取加入日期
    date_pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    date_match = re.search(date_pattern, text)
    if date_match:
        year, month, day = date_match.groups()
        info['加入日期'] = f"{year}-{int(month):02d}-{int(day):02d}"
    
    return info

def parse_work_text(text):
    """解析作品信息文本"""
    info = {
        '学生学号': '',
        '作品名称': '',
        '作品描述': '',
        '技术标签': '',
        '难度等级': '中等',
        '创建日期': datetime.now().strftime('%Y-%m-%d'),
        '预览摘要(100字内)': '',
        '下载文件': ''
    }
    
    # 提取学生学号
    sid_match = re.search(r'学生(\w+)', text)
    if sid_match:
        info['学生学号'] = sid_match.group(1)
    
    # 提取作品名称
    name_match = re.search(r'作品名[：:\'"]?([^\'"，,]+)', text)
    if name_match:
        info['作品名称'] = name_match.group(1).strip()
    
    # 提取技术标签
    tech_tags = []
    text_lower = text.lower()
    
    if 'python' in text_lower:
        tech_tags.append('Python')
    if 'tensorflow' in text_lower:
        tech_tags.append('TensorFlow')
    if 'flask' in text_lower:
        tech_tags.append('Flask')
    if 'html' in text_lower:
        tech_tags.append('HTML')
    if 'css' in text_lower:
        tech_tags.append('CSS')
    if 'javascript' in text_lower or 'js' in text_lower:
        tech_tags.append('JavaScript')
    if 'arduino' in text_lower:
        tech_tags.append('Arduino')
    if 'c++' in text_lower or 'c\+\+' in text_lower:
        tech_tags.append('C++')
    if 'scratch' in text_lower:
        tech_tags.append('Scratch')
    if '深度学习' in text or 'ai' in text_lower:
        tech_tags.append('深度学习')
    
    if tech_tags:
        info['技术标签'] = ','.join(tech_tags)
    
    # 提取作品描述
    desc_match = re.search(r'描述[：:]\s*([^。]+)', text)
    if desc_match:
        info['作品描述'] = desc_match.group(1).strip()
        # 自动生成预览摘要（前50字）
        preview = desc_match.group(1).strip()
        if len(preview) > 100:
            preview = preview[:97] + '...'
        info['预览摘要(100字内)'] = preview
    
    # 提取难度等级
    if '简单' in text or '初级' in text:
        info['难度等级'] = '简单'
    elif '困难' in text or '高级' in text or '复杂' in text:
        info['难度等级'] = '困难'
    
    return info

def add_student_from_text(text):
    """从文本添加学生"""
    ensure_dirs()
    
    # 解析文本
    student_info = parse_student_text(text)
    
    # 生成学号
    student_info['学号'] = generate_next_student_id()
    
    # 读取现有数据
    students = read_csv_as_dict(STUDENT_CSV)
    
    # 添加新学生
    students.append(student_info)
    
    # 写回CSV
    fieldnames = ['学号', '姓名', '年级', '擅长标签', '分类', '个人简介', '加入日期', '头像文件名']
    write_dict_to_csv(STUDENT_CSV, students, fieldnames)
    
    # 创建学生文件夹
    student_dir = STUDENTS_DIR / student_info['学号']
    student_dir.mkdir(exist_ok=True)
    
    print(f"✅ 学生添加成功！")
    print(f"   学号: {student_info['学号']}")
    print(f"   姓名: {student_info['姓名']}")
    print(f"   年级: {student_info['年级']}")
    print(f"   擅长: {student_info['擅长标签']}")
    
    # 更新JSON数据
    update_json_data()
    
    return student_info

def add_work_from_text(text):
    """从文本添加作品"""
    ensure_dirs()
    
    # 解析文本
    work_info = parse_work_text(text)
    
    # 生成作品ID
    work_info['作品ID'] = generate_next_work_id()
    
    # 检查学生是否存在
    students = read_csv_as_dict(STUDENT_CSV)
    student_exists = any(s.get('学号') == work_info['学生学号'] for s in students)
    
    if not student_exists:
        print(f"⚠️  学生 {work_info['学生学号']} 不存在，请先添加学生")
        return None
    
    # 读取现有数据
    works = read_csv_as_dict(WORKS_CSV)
    
    # 添加新作品
    works.append(work_info)
    
    # 写回CSV
    fieldnames = ['作品ID', '学生学号', '作品名称', '作品描述', '技术标签', '难度等级', '创建日期', '预览摘要(100字内)', '下载文件']
    write_dict_to_csv(WORKS_CSV, works, fieldnames)
    
    # 创建作品文件夹
    work_dir = STUDENTS_DIR / work_info['学生学号'] / work_info['作品ID']
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建默认ZIP文件
    zip_filename = f"{work_info['作品ID']}_{work_info['作品名称']}.zip"
    zip_path = DOWNLOADS_DIR / zip_filename
    
    # 创建空ZIP文件（实际使用时应打包实际文件）
    import zipfile
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # 添加一个说明文件
        readme_content = f"""# {work_info['作品名称']}

作者: {work_info['学生学号']}
创建日期: {work_info['创建日期']}
技术标签: {work_info['技术标签']}
难度等级: {work_info['难度等级']}

{work_info['作品描述']}
"""
        zipf.writestr("README.txt", readme_content)
    
    # 更新作品CSV中的下载文件名
    work_info['下载文件'] = zip_filename
    works[-1]['下载文件'] = zip_filename
    write_dict_to_csv(WORKS_CSV, works, fieldnames)
    
    # 添加社交数据
    add_social_data(work_info['作品ID'])
    
    print(f"✅ 作品添加成功！")
    print(f"   作品ID: {work_info['作品ID']}")
    print(f"   作品名: {work_info['作品名称']}")
    print(f"   学生: {work_info['学生学号']}")
    
    # 更新JSON数据
    update_json_data()
    
    return work_info

def add_social_data(work_id):
    """为作品添加社交数据"""
    social_data = read_csv_as_dict(SOCIAL_CSV)
    
    new_social = {
        '作品ID': work_id,
        '点赞数': '0',
        '转发数': '0',
        '星标数': '0',
        '最后更新时间': datetime.now().strftime('%Y-%m-%d')
    }
    
    social_data.append(new_social)
    
    fieldnames = ['作品ID', '点赞数', '转发数', '星标数', '最后更新时间']
    write_dict_to_csv(SOCIAL_CSV, social_data, fieldnames)

def update_json_data():
    """更新JSON数据文件（调用原有的simple_update_data.py）"""
    try:
        # 导入并运行原有的更新脚本
        sys.path.append(str(BASE_DIR))
        from simple_update_data import main as update_main
        update_main()
        print("📊 JSON数据已更新")
    except Exception as e:
        print(f"⚠️  JSON更新失败: {e}")

def interactive_mode():
    """交互式模式"""
    print("🤖 智能表格助手 v1.0")
    print("=" * 40)
    print("支持命令:")
    print("  1. 添加学生 - 输入 '学生: [描述]'")
    print("  2. 添加作品 - 输入 '作品: [描述]'")
    print("  3. 退出 - 输入 '退出' 或 'quit'")
    print("=" * 40)
    
    while True:
        user_input = input("\n📝 请输入: ").strip()
        
        if user_input.lower() in ['退出', 'quit', 'exit', 'q']:
            print("👋 再见！")
            break
        
        if user_input.startswith('学生:'):
            text = user_input[3:].strip()
            add_student_from_text(text)
        
        elif user_input.startswith('作品:'):
            text = user_input[3:].strip()
            add_work_from_text(text)
        
        else:
            # 自动检测类型
            if '学生' in user_input and ('新增' in user_input or '添加' in user_input):
                add_student_from_text(user_input)
            elif '作品' in user_input and ('新增' in user_input or '添加' in user_input):
                add_work_from_text(user_input)
            else:
                print("❓ 无法识别命令，请使用 '学生:' 或 '作品:' 开头")

def batch_mode(text):
    """批量模式：直接处理文本"""
    if '学生' in text and ('新增' in text or '添加' in text):
        return add_student_from_text(text)
    elif '作品' in text and ('新增' in text or '添加' in text):
        return add_work_from_text(text)
    else:
        print("❓ 无法识别内容类型")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        text = ' '.join(sys.argv[1:])
        batch_mode(text)
    else:
        # 交互式模式
        interactive_mode()