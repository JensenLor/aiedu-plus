#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生作品数据更新脚本
功能：读取Excel表格和文件夹结构，生成JSON数据文件
更新频率：每周一次
"""

import os
import json
import pandas as pd
from datetime import datetime
import glob

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")

# 确保生成目录存在
os.makedirs(GENERATED_DIR, exist_ok=True)

def read_csv_data():
    """读取CSV文件数据"""
    try:
        # 读取学生基本信息
        students_csv = os.path.join(BASE_DIR, "学生基本信息.csv")
        students_df = pd.read_csv(students_csv)
        
        # 读取作品信息
        works_csv = os.path.join(BASE_DIR, "作品信息.csv")
        works_df = pd.read_csv(works_csv)
        
        # 读取社交数据（如果有）
        social_csv = os.path.join(BASE_DIR, "社交数据.csv")
        if os.path.exists(social_csv):
            social_df = pd.read_csv(social_csv)
        else:
            social_df = pd.DataFrame(columns=['作品ID', '点赞数', '转发数', '星标数', '最后更新时间'])
        
        return students_df, works_df, social_df
    except Exception as e:
        print(f"读取CSV文件失败: {e}")
        return None, None, None

def scan_student_folders():
    """扫描学生文件夹结构"""
    students_data = []
    
    if not os.path.exists(STUDENTS_DIR):
        print(f"学生文件夹不存在: {STUDENTS_DIR}")
        return students_data
    
    for student_folder in os.listdir(STUDENTS_DIR):
        student_path = os.path.join(STUDENTS_DIR, student_folder)
        if not os.path.isdir(student_path):
            continue
        
        # 解析学号和姓名（格式：学号_姓名）
        parts = student_folder.split('_')
        if len(parts) < 2:
            continue
        
        student_id = parts[0]
        student_name = parts[1]
        
        # 检查头像文件
        avatar_path = os.path.join(student_path, "avatar.jpg")
        avatar_exists = os.path.exists(avatar_path)
        
        # 扫描作品文件夹
        works_dir = os.path.join(student_path, "works")
        works_count = 0
        works_list = []
        
        if os.path.exists(works_dir):
            for work_folder in os.listdir(works_dir):
                work_path = os.path.join(works_dir, work_folder)
                if os.path.isdir(work_path):
                    works_count += 1
                    
                    # 获取作品ID（格式：作品ID_作品名称）
                    work_parts = work_folder.split('_')
                    work_id = work_parts[0] if len(work_parts) > 0 else work_folder
                    
                    # 扫描作品文件
                    work_files = []
                    preview_text = ""
                    
                    for file in os.listdir(work_path):
                        file_path = os.path.join(work_path, file)
                        if os.path.isfile(file_path):
                            file_ext = os.path.splitext(file)[1].lower()
                            file_info = {
                                "name": file,
                                "path": os.path.relpath(file_path, BASE_DIR),
                                "type": get_file_type(file_ext)
                            }
                            work_files.append(file_info)
                            
                            # 读取预览摘要
                            if file == "preview.txt":
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        preview_text = f.read().strip()
                                except:
                                    preview_text = ""
                    
                    works_list.append({
                        "id": work_id,
                        "folder": work_folder,
                        "files": work_files,
                        "preview": preview_text[:100]  # 限制100字
                    })
        
        students_data.append({
            "id": student_id,
            "name": student_name,
            "folder": student_folder,
            "has_avatar": avatar_exists,
            "works_count": works_count,
            "works": works_list
        })
    
    return students_data

def get_file_type(extension):
    """根据扩展名判断文件类型"""
    image_ext = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    video_ext = ['.mp4', '.avi', '.mov', '.wmv', '.flv']
    doc_ext = ['.pdf', '.doc', '.docx', '.txt', '.md']
    code_ext = ['.zip', '.rar', '.7z', '.py', '.js', '.html', '.css']
    
    if extension in image_ext:
        return "image"
    elif extension in video_ext:
        return "video"
    elif extension in doc_ext:
        return "document"
    elif extension in code_ext:
        return "code"
    else:
        return "other"

def generate_json_data(students_df, works_df, social_df, folder_data):
    """生成JSON数据文件"""
    
    # 1. 生成学生JSON
    students_json = []
    if students_df is not None and not students_df.empty:
        for _, row in students_df.iterrows():
            student_id = str(row.get('学号', ''))
            student_name = str(row.get('姓名', ''))
            
            # 查找文件夹数据
            folder_info = None
            for folder_item in folder_data:
                if folder_item['id'] == student_id:
                    folder_info = folder_item
                    break
            
            student_data = {
                "id": student_id,
                "name": student_name,
                "grade": str(row.get('年级', '')),
                "study_months": int(row.get('学习时长(月)', 0)),
                "tags": [tag.strip() for tag in str(row.get('擅长标签', '')).split(',') if tag.strip()],
                "works_count": int(row.get('作品数量', 0)),
                "categories": [cat.strip() for cat in str(row.get('分类', '')).split(',') if cat.strip()],
                "description": str(row.get('个人简介', '')),
                "join_date": str(row.get('加入日期', '')),
                "avatar_file": str(row.get('头像文件名', 'avatar.jpg')),
                "has_avatar": folder_info['has_avatar'] if folder_info else False,
                "folder": folder_info['folder'] if folder_info else f"{student_id}_{student_name}"
            }
            students_json.append(student_data)
    
    # 2. 生成作品JSON
    works_json = []
    if works_df is not None and not works_df.empty:
        for _, row in works_df.iterrows():
            work_data = {
                "id": str(row.get('作品ID', '')),
                "student_id": str(row.get('学生学号', '')),
                "title": str(row.get('作品名称', '')),
                "description": str(row.get('作品描述', '')),
                "tech_tags": [tag.strip() for tag in str(row.get('技术标签', '')).split(',') if tag.strip()],
                "difficulty": str(row.get('难度等级', '中等')),
                "github_url": str(row.get('GitHub链接', '')),
                "created_date": str(row.get('创建日期', '')),
                "preview_summary": str(row.get('预览摘要(100字内)', ''))[:100]
            }
            works_json.append(work_data)
    
    # 3. 生成社交JSON
    social_json = {}
    if social_df is not None and not social_df.empty:
        for _, row in social_df.iterrows():
            work_id = str(row.get('作品ID', ''))
            social_json[work_id] = {
                "likes": int(row.get('点赞数', 0)),
                "shares": int(row.get('转发数', 0)),
                "stars": int(row.get('星标数', 0)),
                "last_updated": str(row.get('最后更新时间', datetime.now().strftime('%Y-%m-%d')))
            }
    
    # 4. 生成汇总数据
    summary = {
        "total_students": len(students_json),
        "total_works": len(works_json),
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "update_frequency": "每周一次"
    }
    
    return {
        "students": students_json,
        "works": works_json,
        "social": social_json,
        "summary": summary
    }

def save_json_files(data):
    """保存JSON文件到generated目录"""
    
    # 1. 保存完整的整合数据
    with open(os.path.join(GENERATED_DIR, "data.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 2. 分别保存各个数据文件
    with open(os.path.join(GENERATED_DIR, "students.json"), 'w', encoding='utf-8') as f:
        json.dump(data["students"], f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(GENERATED_DIR, "works.json"), 'w', encoding='utf-8') as f:
        json.dump(data["works"], f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(GENERATED_DIR, "social.json"), 'w', encoding='utf-8') as f:
        json.dump(data["social"], f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(GENERATED_DIR, "summary.json"), 'w', encoding='utf-8') as f:
        json.dump(data["summary"], f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到: {GENERATED_DIR}")
    print(f"学生数量: {data['summary']['total_students']}")
    print(f"作品数量: {data['summary']['total_works']}")
    print(f"更新时间: {data['summary']['last_updated']}")

def main():
    """主函数"""
    print("开始更新学生作品数据...")
    print(f"数据目录: {BASE_DIR}")
    print(f"学生文件夹: {STUDENTS_DIR}")
    
    # 读取CSV数据
    students_df, works_df, social_df = read_csv_data()
    if students_df is None:
        print("错误: 无法读取CSV文件，请检查文件格式和路径")
        return
    
    # 扫描文件夹结构
    folder_data = scan_student_folders()
    
    # 生成JSON数据
    json_data = generate_json_data(students_df, works_df, social_df, folder_data)
    
    # 保存JSON文件
    save_json_files(json_data)
    
    print("数据更新完成！")

if __name__ == "__main__":
    main()