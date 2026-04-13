#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作品打包脚本 - 自动为每个作品创建ZIP下载包
"""

import os
import zipfile
import shutil
from datetime import datetime

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")
ZIP_DIR = os.path.join(BASE_DIR, "downloads")

def create_downloads_directory():
    """创建下载目录"""
    os.makedirs(ZIP_DIR, exist_ok=True)
    print(f"下载目录已创建: {ZIP_DIR}")

def create_zip_for_work(student_folder, work_folder, zip_filename):
    """为单个作品创建ZIP包"""
    work_path = os.path.join(STUDENTS_DIR, student_folder, "works", work_folder)
    zip_path = os.path.join(ZIP_DIR, zip_filename)
    
    if not os.path.exists(work_path):
        print(f"作品文件夹不存在: {work_path}")
        return False
    
    try:
        # 创建ZIP文件
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历作品文件夹中的所有文件和子文件夹
            for root, dirs, files in os.walk(work_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算在ZIP中的相对路径
                    arcname = os.path.relpath(file_path, work_path)
                    zipf.write(file_path, arcname)
        
        print(f"已创建ZIP包: {zip_filename} ({os.path.getsize(zip_path)/1024:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"创建ZIP包失败 {work_folder}: {e}")
        return False

def scan_and_create_zips():
    """扫描所有作品并创建ZIP包"""
    create_downloads_directory()
    
    if not os.path.exists(STUDENTS_DIR):
        print(f"学生文件夹不存在: {STUDENTS_DIR}")
        return []
    
    created_zips = []
    
    for student_folder in os.listdir(STUDENTS_DIR):
        student_path = os.path.join(STUDENTS_DIR, student_folder)
        if not os.path.isdir(student_path):
            continue
        
        # 解析学号和姓名
        parts = student_folder.split('_')
        if len(parts) < 2:
            continue
        
        student_id = parts[0].strip()
        
        # 扫描作品文件夹
        works_dir = os.path.join(student_path, "works")
        if not os.path.exists(works_dir):
            continue
        
        for work_folder in os.listdir(works_dir):
            work_path = os.path.join(works_dir, work_folder)
            if not os.path.isdir(work_path):
                continue
            
            # 获取作品ID（格式：作品ID_作品名称）
            work_parts = work_folder.split('_')
            work_id = work_parts[0].strip() if len(work_parts) > 0 else work_folder.strip()
            
            # 生成ZIP文件名
            zip_filename = f"{work_folder}.zip"
            
            # 创建ZIP包
            if create_zip_for_work(student_folder, work_folder, zip_filename):
                created_zips.append({
                    "work_id": work_id,
                    "work_folder": work_folder,
                    "zip_file": zip_filename,
                    "student_id": student_id
                })
    
    return created_zips

def update_csv_with_zip_files(zip_list):
    """更新作品信息CSV，添加下载文件字段"""
    csv_path = os.path.join(BASE_DIR, "作品信息.csv")
    
    if not os.path.exists(csv_path):
        print(f"作品信息CSV文件不存在: {csv_path}")
        return False
    
    try:
        import csv
        
        # 读取现有数据
        rows = []
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(row)
        
        # 创建ZIP文件映射
        zip_mapping = {item["work_id"]: item["zip_file"] for item in zip_list}
        
        # 更新每行数据
        for row in rows:
            work_id = row.get('作品ID', '').strip()
            if work_id in zip_mapping:
                row['下载文件'] = zip_mapping[work_id]
            else:
                # 如果没有对应的ZIP，生成一个默认的
                work_name = row.get('作品名称', '').strip().replace(' ', '_')
                row['下载文件'] = f"{work_id}_{work_name}.zip"
        
        # 确保字段名包含下载文件
        if '下载文件' not in fieldnames:
            fieldnames.append('下载文件')
        
        # 写回文件
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"已更新作品信息CSV: {csv_path}")
        return True
        
    except Exception as e:
        print(f"更新CSV文件失败: {e}")
        return False

def main():
    """主函数"""
    print("开始创建作品ZIP下载包...")
    print(f"学生文件夹: {STUDENTS_DIR}")
    print(f"下载目录: {ZIP_DIR}")
    
    # 扫描并创建ZIP包
    created_zips = scan_and_create_zips()
    
    if created_zips:
        print(f"\n成功创建 {len(created_zips)} 个ZIP包:")
        for zip_info in created_zips:
            print(f"  - {zip_info['work_id']}: {zip_info['zip_file']}")
        
        # 更新CSV文件
        update_csv_with_zip_files(created_zips)
    else:
        print("未找到可打包的作品文件夹")
    
    print("\nZIP包创建完成！")
    print(f"下载目录: {ZIP_DIR}")

if __name__ == "__main__":
    main()