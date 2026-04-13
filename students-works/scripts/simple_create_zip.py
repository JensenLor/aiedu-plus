#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单作品打包脚本
"""

import os
import zipfile
import shutil

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")
ZIP_DIR = os.path.join(BASE_DIR, "downloads")

# 创建下载目录
os.makedirs(ZIP_DIR, exist_ok=True)
print(f"下载目录: {ZIP_DIR}")

# 作品文件夹路径
work_folder = "work001_智能天气助手"
student_folder = "zzy001_曾梓扬"
work_path = os.path.join(STUDENTS_DIR, student_folder, "works", work_folder)
zip_filename = f"{work_folder}.zip"
zip_path = os.path.join(ZIP_DIR, zip_filename)

# 检查作品文件夹是否存在
if not os.path.exists(work_path):
    print(f"错误: 作品文件夹不存在: {work_path}")
    exit(1)

print(f"作品文件夹: {work_path}")

# 创建ZIP文件
try:
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历作品文件夹中的所有文件
        for root, dirs, files in os.walk(work_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 计算在ZIP中的相对路径
                arcname = os.path.relpath(file_path, work_path)
                zipf.write(file_path, arcname)
                print(f"  添加: {arcname}")
    
    file_size = os.path.getsize(zip_path)
    print(f"\n成功创建ZIP包: {zip_filename}")
    print(f"文件大小: {file_size/1024:.1f} KB")
    print(f"保存位置: {zip_path}")
    
except Exception as e:
    print(f"创建ZIP包失败: {e}")
    exit(1)