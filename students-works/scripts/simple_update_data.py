#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生作品数据更新脚本（增强版）
支持扫描证书和作品封面
"""

import os
import json
import csv
from datetime import datetime
import glob

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")

# 确保生成目录存在
os.makedirs(GENERATED_DIR, exist_ok=True)

def read_csv_file(file_path):
    """读取CSV文件，返回字典列表"""
    if not os.path.exists(file_path):
        print(f"警告: 文件不存在 {file_path}")
        return []
    
    data = []
    try:
        # 尝试不同编码
        encodings = ['utf-8-sig', 'gbk', 'gb2312', 'latin-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # 清理字典值，去除可能的空格
                        cleaned_row = {}
                        for key, value in row.items():
                            if key and value:
                                cleaned_row[key.strip()] = value.strip() if isinstance(value, str) else value
                        if cleaned_row:
                            data.append(cleaned_row)
                print(f"使用编码 {encoding} 成功读取 {file_path}")
                return data
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"编码 {encoding} 读取失败: {e}")
                continue
        
        print(f"所有编码尝试失败 {file_path}")
        return []
    except Exception as e:
        print(f"读取CSV文件失败 {file_path}: {e}")
        return []

def read_csv_data():
    """读取所有CSV文件数据"""
    # 读取学生基本信息
    students_csv = os.path.join(BASE_DIR, "学生基本信息.csv")
    students_data = read_csv_file(students_csv)
    
    # 读取作品信息
    works_csv = os.path.join(BASE_DIR, "作品信息.csv")
    works_data = read_csv_file(works_csv)
    
    # 读取社交数据（可选）
    social_csv = os.path.join(BASE_DIR, "社交数据.csv")
    social_data = read_csv_file(social_csv)
    
    return {
        "students": students_data,
        "works": works_data,
        "social": social_data
    }

def calculate_study_months(join_date_str):
    """根据加入日期计算学习时长（月）"""
    try:
        join_date = datetime.strptime(join_date_str, "%Y-%m-%d")
        today = datetime.now()
        
        # 计算月份差
        months = (today.year - join_date.year) * 12 + (today.month - join_date.month)
        # 如果天数差小于0，月份减1
        if today.day < join_date.day:
            months -= 1
        # 确保至少为0
        return max(0, months)
    except Exception as e:
        print(f"计算学习时长失败 {join_date_str}: {e}")
        return 0

def count_student_works(works_data, student_id):
    """统计学生作品数量"""
    count = 0
    for work in works_data:
        if work.get("学生学号") == student_id:
            count += 1
    return count

def scan_student_folders(students_data, works_data):
    """扫描学生文件夹，收集额外信息"""
    print("扫描学生文件夹...")
    
    for student in students_data:
        student_id = student.get("学号")
        student_name = student.get("姓名")
        
        if not student_id or not student_name:
            continue
            
        # 构建学生文件夹路径
        folder_name = f"{student_id}_{student_name}"
        student_folder = os.path.join(STUDENTS_DIR, folder_name)
        
        # 检查文件夹是否存在
        if not os.path.exists(student_folder):
            print(f"  {student_id}: 文件夹不存在 ({folder_name})")
            continue
            
        # 扫描证书文件夹
        certs_dir = os.path.join(student_folder, "certificates")
        certificates = []
        if os.path.exists(certs_dir):
            cert_files = glob.glob(os.path.join(certs_dir, "*"))
            for cert_file in cert_files:
                if os.path.isfile(cert_file):
                    file_ext = os.path.splitext(cert_file)[1].lower()
                    if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf']:
                        cert_name = os.path.basename(cert_file)
                        certificates.append({
                            "file": cert_name,
                            "path": f"students/{folder_name}/certificates/{cert_name}",
                            "type": "pdf" if file_ext == '.pdf' else "image"
                        })
        
        # 扫描作品文件夹，查找封面图
        works_dir = os.path.join(student_folder, "works")
        if os.path.exists(works_dir):
            # 扫描每个作品子文件夹
            work_folders = []
            for item in os.listdir(works_dir):
                work_folder_path = os.path.join(works_dir, item)
                if os.path.isdir(work_folder_path):
                    # 查找封面图
                    cover_image = None
                    for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                        cover_path = os.path.join(work_folder_path, f"cover{ext}")
                        if os.path.exists(cover_path):
                            cover_image = f"cover{ext}"
                            break
                    
                    work_folders.append({
                        "name": item,
                        "cover_image": cover_image
                    })
        
        # 检查头像文件
        avatar_files = glob.glob(os.path.join(student_folder, "avatar.*"))
        has_avatar = len(avatar_files) > 0
        avatar_file = "default_avatar.jpg"
        if has_avatar:
            avatar_file = os.path.basename(avatar_files[0])
        
        # 添加到学生数据
        student["certificates"] = certificates
        student["has_avatar"] = has_avatar
        student["avatar_file"] = avatar_file
    
    return students_data

def generate_students_json(students_data, works_data):
    """生成学生JSON数据"""
    print("生成学生JSON数据...")
    
    students_list = []
    for student in students_data:
        student_id = student.get("学号")
        
        # 解析擅长标签
        tags_str = student.get("擅长标签", "")
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []
        
        # 解析分类
        categories_str = student.get("分类", "")
        categories = [cat.strip() for cat in categories_str.split(",") if cat.strip()] if categories_str else []
        
        # 计算学习时长
        study_months = calculate_study_months(student.get("加入日期", ""))
        
        # 统计作品数量
        works_count = count_student_works(works_data, student_id)
        
        # 构建学生对象
        student_obj = {
            "id": student_id,
            "name": student.get("姓名"),
            "grade": student.get("年级"),
            "study_months": study_months,
            "tags": tags,
            "works_count": works_count,
            "categories": categories,
            "description": student.get("个人简介", ""),
            "join_date": student.get("加入日期"),
            "avatar_file": student.get("avatar_file", "default_avatar.jpg"),
            "has_avatar": student.get("has_avatar", False),
            "certificates": student.get("certificates", [])
        }
        students_list.append(student_obj)
    
    # 保存到文件
    output_path = os.path.join(GENERATED_DIR, "students.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(students_list, f, ensure_ascii=False, indent=2)
        print(f"  已保存: {output_path}")
        print(f"  学生总数: {len(students_list)}")
    except Exception as e:
        print(f"保存学生JSON失败: {e}")

def generate_works_json(works_data):
    """生成作品JSON数据"""
    print("生成作品JSON数据...")
    
    works_list = []
    work_id_counter = 1
    
    for work in works_data:
        # 生成作品ID
        work_id = f"work{work_id_counter:03d}"
        
        # 解析技术标签
        tech_tags_str = work.get("技术标签", "")
        tech_tags = [tag.strip() for tag in tech_tags_str.split(",") if tag.strip()] if tech_tags_str else []
        
        # 构建作品对象
        work_obj = {
            "id": work_id,
            "student_id": work.get("学生学号"),
            "title": work.get("作品名称"),
            "description": work.get("作品描述", ""),
            "tech_tags": tech_tags,
            "difficulty": work.get("难度等级", "中等"),
            "created_date": work.get("创建日期", ""),
            "preview_summary": work.get("预览摘要", ""),
            "download_file": work.get("下载文件名", "")
        }
        works_list.append(work_obj)
        work_id_counter += 1
    
    # 保存到文件
    output_path = os.path.join(GENERATED_DIR, "works.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(works_list, f, ensure_ascii=False, indent=2)
        print(f"  已保存: {output_path}")
        print(f"  作品总数: {len(works_list)}")
    except Exception as e:
        print(f"保存作品JSON失败: {e}")

def generate_social_json(social_data):
    """生成社交JSON数据"""
    if not social_data:
        print("无社交数据，跳过生成社交JSON")
        return
    
    print("生成社交JSON数据...")
    
    # 保存到文件
    output_path = os.path.join(GENERATED_DIR, "social.json")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(social_data, f, ensure_ascii=False, indent=2)
        print(f"  已保存: {output_path}")
    except Exception as e:
        print(f"保存社交JSON失败: {e}")

def main():
    print("开始更新学生作品数据...")
    print("=" * 50)
    
    # 读取CSV数据
    csv_data = read_csv_data()
    students_data = csv_data["students"]
    works_data = csv_data["works"]
    social_data = csv_data["social"]
    
    print(f"读取到 {len(students_data)} 名学生，{len(works_data)} 个作品")
    
    # 扫描学生文件夹，获取证书、封面图等信息
    students_data = scan_student_folders(students_data, works_data)
    
    # 生成JSON文件
    generate_students_json(students_data, works_data)
    generate_works_json(works_data)
    generate_social_json(social_data)
    
    print("=" * 50)
    print("数据更新完成！")
    print("")
    print("使用说明：")
    print("1. 证书文件应放在：students/学号_姓名/certificates/ 文件夹下")
    print("2. 作品封面图应命名为：cover.jpg (或 .png, .gif)")
    print("3. 学生头像应命名为：avatar.jpg (或 .png)")
    print("4. 网站会自动加载这些文件")

if __name__ == "__main__":
    main()