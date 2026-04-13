#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生作品数据生成脚本 v2
核心逻辑：以文件夹为主数据源，CSV为补充信息
- ID和姓名：从文件夹名自动提取（格式：学号_姓名）
- 补充信息（年级、标签等）：从CSV读取，用学号关联
- 作品数量：从文件夹自动统计
- 学习时长：从加入日期自动计算
"""

import os
import json
import csv
import glob
from datetime import datetime

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDENTS_DIR = os.path.join(BASE_DIR, "students")
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")

# 确保目录存在
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def read_csv_file(file_path):
    """读取CSV文件，返回以学号为键的字典"""
    if not os.path.exists(file_path):
        print(f"  跳过(不存在): {file_path}")
        return {}

    data = {}
    encodings = ['utf-8-sig', 'gbk', 'gb2312', 'latin-1']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned = {}
                    for key, value in row.items():
                        if key and value is not None:
                            cleaned[key.strip()] = value.strip() if isinstance(value, str) else value
                    # 用学号作为键
                    student_id = cleaned.get("学号", "")
                    if student_id:
                        data[student_id] = cleaned
            print(f"  读取成功: {file_path} ({len(data)}条, 编码:{encoding})")
            return data
        except (UnicodeDecodeError, Exception):
            continue

    print(f"  读取失败: {file_path}")
    return {}


def calculate_study_months(join_date_str):
    """根据加入日期自动计算学习时长（月）"""
    if not join_date_str or join_date_str == 'nan':
        return 0

    # 尝试多种日期格式
    date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"]
    for fmt in date_formats:
        try:
            join_date = datetime.strptime(join_date_str, fmt)
            today = datetime.now()
            months = (today.year - join_date.year) * 12 + (today.month - join_date.month)
            if today.day < join_date.day:
                months -= 1
            return max(0, months)
        except ValueError:
            continue
    return 0


def parse_folder_name(folder_name):
    """从文件夹名解析学号和姓名
    支持格式：ZZS0001_曾梓扬, ZZS0001_曾梓扬_备注
    """
    parts = folder_name.split('_', 1)
    if len(parts) >= 2:
        return parts[0], parts[1]
    return folder_name, ""


def read_work_info_file(work_folder_path):
    """从作品文件夹中读取 info.txt 补充信息"""
    info_path = os.path.join(work_folder_path, "info.txt")
    if not os.path.exists(info_path):
        return {}

    info = {}
    try:
        with open(info_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
                elif line and not info.get('description'):
                    # 没有键值对的行作为描述
                    info['description'] = line
    except Exception:
        pass
    return info


def scan_students():
    """核心函数：扫描学生文件夹，生成数据"""
    print("\n[1/3] 扫描学生文件夹...")

    if not os.path.exists(STUDENTS_DIR):
        print(f"  错误: 学生文件夹不存在 {STUDENTS_DIR}")
        return [], []

    # 读取CSV补充数据
    students_csv = read_csv_file(os.path.join(BASE_DIR, "学生基本信息.csv"))

    # 作品CSV以"作品ID"为键（作品CSV没有"学号"列，需要特殊处理）
    works_csv = {}
    works_csv_path = os.path.join(BASE_DIR, "作品信息.csv")
    if os.path.exists(works_csv_path):
        encodings = ['utf-8-sig', 'gbk', 'gb2312', 'latin-1']
        for encoding in encodings:
            try:
                with open(works_csv_path, 'r', encoding=encoding) as f:
                    reader = csv.DictReader(f)
                    count = 0
                    for row in reader:
                        cleaned = {}
                        for key, value in row.items():
                            if key and value is not None:
                                cleaned[key.strip()] = value.strip() if isinstance(value, str) else value
                        work_id = cleaned.get("作品ID", "")
                        if work_id:
                            works_csv[work_id] = cleaned
                            count += 1
                    print(f"  读取成功: {works_csv_path} ({count}条, 编码:{encoding})")
                break
            except (UnicodeDecodeError, Exception):
                continue

    students_list = []
    works_list = []

    # 遍历学生文件夹
    student_folders = sorted([
        f for f in os.listdir(STUDENTS_DIR)
        if os.path.isdir(os.path.join(STUDENTS_DIR, f))
    ])

    for folder_name in student_folders:
        student_id, student_name = parse_folder_name(folder_name)
        student_path = os.path.join(STUDENTS_DIR, folder_name)

        if not student_id:
            print(f"  跳过(无法解析): {folder_name}")
            continue

        print(f"  处理: {student_id} {student_name}")

        # 获取CSV补充信息
        csv_info = students_csv.get(student_id, {})

        # 头像
        avatar_files = glob.glob(os.path.join(student_path, "avatar.*"))
        has_avatar = len(avatar_files) > 0
        avatar_file = os.path.basename(avatar_files[0]) if has_avatar else "default_avatar.jpg"

        # 证书
        certificates = []
        certs_dir = os.path.join(student_path, "certificates")
        if os.path.exists(certs_dir):
            for cert_file in sorted(glob.glob(os.path.join(certs_dir, "*"))):
                if os.path.isfile(cert_file):
                    ext = os.path.splitext(cert_file)[1].lower()
                    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf']:
                        cert_name = os.path.basename(cert_file)
                        certificates.append({
                            "file": cert_name,
                            "path": f"students/{folder_name}/certificates/{cert_name}",
                            "type": "pdf" if ext == '.pdf' else "image"
                        })

        # 解析标签和分类
        tags_str = csv_info.get("擅长标签", "")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []
        categories_str = csv_info.get("分类", "")
        categories = [c.strip() for c in categories_str.split(",") if c.strip()] if categories_str else []

        # 计算学习时长
        join_date = csv_info.get("加入日期", "")
        study_months = calculate_study_months(join_date)

        # 扫描作品
        works_dir = os.path.join(student_path, "works")
        student_works = []

        if os.path.exists(works_dir):
            for work_folder in sorted(os.listdir(works_dir)):
                work_path = os.path.join(works_dir, work_folder)
                if not os.path.isdir(work_path):
                    continue

                # 从文件夹名解析作品ID和名称
                work_parts = work_folder.split('_', 1)
                work_id = work_parts[0]
                work_title = work_parts[1] if len(work_parts) > 1 else work_folder

                # 读取info.txt补充信息
                info = read_work_info_file(work_path)

                # 读取CSV补充信息（用作品ID匹配）
                csv_work_info = {}
                if work_id:
                    for wid, wdata in works_csv.items():
                        if wid == work_id:
                            csv_work_info = wdata
                            break
                    # 也按作品名称匹配
                    if not csv_work_info:
                        for wid, wdata in works_csv.items():
                            if wdata.get("作品名称", "") == work_title:
                                csv_work_info = wdata
                                break

                # 优先使用CSV信息，info.txt次之
                description = csv_work_info.get("作品描述", "") or info.get("description", "")
                difficulty = csv_work_info.get("难度等级", "") or info.get("difficulty", "中等")
                created_date = csv_work_info.get("创建日期", "") or info.get("date", "")
                preview_summary = csv_work_info.get("预览摘要(100字内)", "") or info.get("preview", "")

                # 技术标签：CSV优先，info.txt次之
                tech_tags_str = csv_work_info.get("技术标签", "") or info.get("tags", "")
                tech_tags = [t.strip() for t in tech_tags_str.split(",") if t.strip()] if tech_tags_str else []

                # 下载文件
                download_file = csv_work_info.get("下载文件", "") or csv_work_info.get("下载文件名", "")
                if not download_file:
                    # 自动查找ZIP文件
                    zip_files = glob.glob(os.path.join(DOWNLOADS_DIR, f"{work_id}*.zip"))
                    if zip_files:
                        download_file = os.path.basename(zip_files[0])

                # 封面图
                cover_image = None
                for ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    if os.path.exists(os.path.join(work_path, f"cover{ext}")):
                        cover_image = f"cover{ext}"
                        break

                work_obj = {
                    "id": work_id,
                    "student_id": student_id,
                    "title": work_title,
                    "description": description,
                    "tech_tags": tech_tags,
                    "difficulty": difficulty or "中等",
                    "created_date": created_date,
                    "preview_summary": preview_summary[:100] if preview_summary else "",
                    "download_file": download_file,
                    "folder": work_folder,
                    "cover_image": cover_image
                }
                works_list.append(work_obj)
                student_works.append(work_obj)

        # 构建学生对象
        student_obj = {
            "id": student_id,
            "name": student_name or csv_info.get("姓名", ""),
            "grade": csv_info.get("年级", ""),
            "study_months": study_months,
            "tags": tags,
            "works_count": len(student_works),
            "categories": categories,
            "description": csv_info.get("个人简介", ""),
            "join_date": join_date,
            "avatar_file": avatar_file,
            "has_avatar": has_avatar,
            "certificates": certificates
        }
        students_list.append(student_obj)

    print(f"  完成: {len(students_list)} 名学生, {len(works_list)} 个作品")
    return students_list, works_list


def save_json(students, works):
    """保存JSON文件"""
    print("\n[2/3] 生成JSON文件...")

    # students.json
    path = os.path.join(GENERATED_DIR, "students.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)
    print(f"  students.json ({len(students)}条)")

    # works.json
    path = os.path.join(GENERATED_DIR, "works.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(works, f, ensure_ascii=False, indent=2)
    print(f"  works.json ({len(works)}条)")

    # summary.json
    summary = {
        "total_students": len(students),
        "total_works": len(works),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": "folder-first"
    }
    path = os.path.join(GENERATED_DIR, "summary.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"  summary.json")


def print_summary(students, works):
    """打印汇总信息"""
    print("\n[3/3] 数据汇总")
    print("=" * 50)
    print(f"  学生总数: {len(students)}")
    print(f"  作品总数: {len(works)}")
    print(f"  有作品的学生: {len(set(w['student_id'] for w in works))}")
    print(f"  有CSV信息的学生: {sum(1 for s in students if s['grade'])}")
    print(f"  有证书的学生: {sum(1 for s in students if s['certificates'])}")
    print("=" * 50)
    print("\n学生列表:")
    for s in students:
        status = "V" if s['grade'] else "O"
        works_n = s['works_count']
        print(f"  {status} {s['id']} {s['name']} | {s['grade'] or '未填写年级'} | {works_n}个作品 | {s['study_months']}月")
    print()


def main():
    print("学生作品数据生成 v2 (文件夹优先)")
    print("=" * 50)
    print(f"数据目录: {BASE_DIR}")

    students, works = scan_students()
    save_json(students, works)
    print_summary(students, works)

    print("完成！网站刷新即可看到更新。")


if __name__ == "__main__":
    main()
