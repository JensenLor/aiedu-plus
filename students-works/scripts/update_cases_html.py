#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新cases.html页面的脚本
根据生成的数据文件自动更新学生作品展示页面
"""

import os
import json
from datetime import datetime

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_DIR = os.path.join(BASE_DIR, "generated")
CASES_HTML = os.path.join(os.path.dirname(BASE_DIR), "cases.html")

def load_json_data():
    """加载生成的JSON数据"""
    data_files = {
        "students": os.path.join(GENERATED_DIR, "students.json"),
        "works": os.path.join(GENERATED_DIR, "works.json"),
        "social": os.path.join(GENERATED_DIR, "social.json")
    }
    
    data = {}
    for key, file_path in data_files.items():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data[key] = json.load(f)
        except FileNotFoundError:
            print(f"警告: 文件不存在 {file_path}")
            data[key] = []
        except json.JSONDecodeError:
            print(f"错误: JSON解析失败 {file_path}")
            data[key] = []
    
    return data

def generate_student_card(student, works_data, social_data):
    """生成单个学生卡片HTML"""
    student_id = student.get('id', '')
    student_name = student.get('name', '')
    grade = student.get('grade', '')
    study_months = student.get('study_months', 0)
    tags = student.get('tags', [])
    categories = student.get('categories', [])
    works_count = student.get('works_count', 0)
    
    # 计算学生总热度（所有作品的热度之和）
    total_likes = 0
    total_shares = 0
    total_stars = 0
    
    # 查找该学生的作品
    student_works = [work for work in works_data if work.get('student_id') == student_id]
    for work in student_works:
        work_id = work.get('id', '')
        if work_id in social_data:
            total_likes += social_data[work_id].get('likes', 0)
            total_shares += social_data[work_id].get('shares', 0)
            total_stars += social_data[work_id].get('stars', 0)
    
    # 生成标签HTML
    tags_html = ""
    for tag in tags[:3]:  # 最多显示3个标签
        tags_html += f'<span class="student-tag">{tag}</span>'
    
    # 生成分类数据属性
    category_attr = " ".join(categories) if categories else "all"
    
    # 生成热度显示
    heat_html = ""
    if total_likes > 0 or total_shares > 0 or total_stars > 0:
        heat_html = f'''
        <div class="student-heat">
            <div class="heat-item">
                <i class="fas fa-fire"></i>
                <span>热度：</span>
            </div>
            <div class="heat-stats">
                <span class="heat-stat"><i class="fas fa-star"></i> {total_stars}</span>
                <span class="heat-stat"><i class="fas fa-thumbs-up"></i> {total_likes}</span>
                <span class="heat-stat"><i class="fas fa-share"></i> {total_shares}</span>
            </div>
        </div>'''
    
    # 生成学生卡片HTML
    card_html = f'''
            <div class="student-card" data-category="{category_attr}" data-student-id="{student_id}">
                <div class="student-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <div class="student-info">
                    <h3 class="student-name">{student_name}</h3>
                    <div class="student-grade">
                        <i class="fas fa-graduation-cap"></i>
                        <span>{grade} | 学习时间：{study_months}个月</span>
                    </div>
                    <div class="student-tags">
                        {tags_html}
                    </div>
                    <div class="works-count">
                        <i class="fas fa-folder-open"></i>
                        <span>{works_count}个作品</span>
                    </div>
                    {heat_html}
                </div>
            </div>'''
    
    return card_html

def generate_work_preview_modal(works_data, social_data):
    """生成作品预览模态框的HTML"""
    modals_html = ""
    
    for work in works_data:
        work_id = work.get('id', '')
        title = work.get('title', '')
        description = work.get('description', '')
        preview_summary = work.get('preview_summary', '')
        tech_tags = work.get('tech_tags', [])
        difficulty = work.get('difficulty', '中等')
        github_url = work.get('github_url', '')
        created_date = work.get('created_date', '')
        
        # 获取社交数据
        likes = social_data.get(work_id, {}).get('likes', 0)
        shares = social_data.get(work_id, {}).get('shares', 0)
        stars = social_data.get(work_id, {}).get('stars', 0)
        
        # 生成技术标签HTML
        tech_tags_html = ""
        for tag in tech_tags:
            tech_tags_html += f'<span class="tech-tag">{tag}</span>'
        
        # 生成难度标签样式
        difficulty_class = {
            '简单': 'difficulty-easy',
            '中等': 'difficulty-medium',
            '困难': 'difficulty-hard'
        }.get(difficulty, 'difficulty-medium')
        
        modal_html = f'''
        <div id="preview-modal-{work_id}" class="preview-modal" style="display: none;">
            <div class="preview-modal-content">
                <div class="preview-header">
                    <h3>{title}</h3>
                    <button class="close-modal" onclick="closePreviewModal('{work_id}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="preview-body">
                    <div class="preview-summary">
                        <p>{preview_summary}</p>
                    </div>
                    <div class="preview-details">
                        <div class="detail-item">
                            <i class="fas fa-info-circle"></i>
                            <strong>作品描述：</strong>
                            <p>{description}</p>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-code"></i>
                            <strong>技术栈：</strong>
                            <div class="tech-tags">
                                {tech_tags_html}
                            </div>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-chart-line"></i>
                            <strong>难度等级：</strong>
                            <span class="difficulty-badge {difficulty_class}">{difficulty}</span>
                        </div>
                        <div class="detail-item">
                            <i class="fab fa-github"></i>
                            <strong>GitHub：</strong>
                            <a href="{github_url}" target="_blank">{github_url if github_url else '暂无链接'}</a>
                        </div>
                        <div class="detail-item">
                            <i class="fas fa-calendar"></i>
                            <strong>创建时间：</strong>
                            <span>{created_date}</span>
                        </div>
                    </div>
                    <div class="preview-social">
                        <div class="social-stats">
                            <div class="social-stat">
                                <i class="fas fa-thumbs-up"></i>
                                <span>点赞：{likes}</span>
                            </div>
                            <div class="social-stat">
                                <i class="fas fa-star"></i>
                                <span>星标：{stars}</span>
                            </div>
                            <div class="social-stat">
                                <i class="fas fa-share"></i>
                                <span>转发：{shares}</span>
                            </div>
                        </div>
                        <div class="social-actions">
                            <button class="social-btn like-btn" data-work-id="{work_id}">
                                <i class="fas fa-thumbs-up"></i> 点赞
                            </button>
                            <button class="social-btn star-btn" data-work-id="{work_id}">
                                <i class="fas fa-star"></i> 星标
                            </button>
                            <button class="social-btn share-btn" data-work-id="{work_id}">
                                <i class="fas fa-share"></i> 转发
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>'''
        
        modals_html += modal_html
    
    return modals_html

def update_cases_html(data):
    """更新cases.html文件"""
    try:
        with open(CASES_HTML, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到文件 {CASES_HTML}")
        return
    
    students_data = data.get('students', [])
    works_data = data.get('works', [])
    social_data = data.get('social', {})
    
    # 生成学生卡片HTML
    student_cards_html = ""
    for student in students_data:
        student_cards_html += generate_student_card(student, works_data, social_data)
    
    # 生成作品预览模态框
    preview_modals_html = generate_work_preview_modal(works_data, social_data)
    
    # 查找并替换学生画廊区域
    # 查找 <!-- 学生画廊 --> 到 <!-- 作品预览模态框 --> 之间的内容
    gallery_start = content.find('<!-- 学生画廊 -->')
    gallery_end = content.find('<!-- 作品预览模态框 -->')
    
    if gallery_start != -1 and gallery_end != -1:
        # 构建新的学生画廊部分
        new_gallery_section = f'''        <!-- 学生画廊 -->
        <div class="student-gallery" id="student-gallery">
            {student_cards_html}
        </div>
        
        <!-- 作品预览模态框 -->
        {preview_modals_html}'''
        
        # 替换内容
        content = content[:gallery_start] + new_gallery_section + content[gallery_end:]
        
        # 更新最后更新时间
        update_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        content = content.replace('最后更新：系统自动更新', f'最后更新：{update_time}')
        
        # 保存更新后的文件
        with open(CASES_HTML, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"成功更新 {CASES_HTML}")
        print(f"更新了 {len(students_data)} 个学生卡片")
        print(f"更新了 {len(works_data)} 个作品预览")
    else:
        print("错误: 找不到替换标记")
        print("请确保cases.html中包含以下注释标记:")
        print("<!-- 学生画廊 -->")
        print("<!-- 作品预览模态框 -->")

def main():
    """主函数"""
    print("开始更新cases.html页面...")
    
    # 加载数据
    data = load_json_data()
    
    if not data['students']:
        print("警告: 没有学生数据，请先运行update_data.py生成数据")
    
    # 更新HTML文件
    update_cases_html(data)
    
    print("页面更新完成！")

if __name__ == "__main__":
    main()