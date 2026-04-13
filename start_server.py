#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的HTTP服务器，用于测试网站
"""

import http.server
import socketserver
import socket
import os
import sys

# 获取本机IP地址
def get_ip_address():
    try:
        # 创建一个socket连接到一个外部地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# 设置端口
PORT = 8000

# 切换到当前目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 创建HTTP服务器
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    ip = get_ip_address()
    print("=" * 60)
    print("网站服务器已启动！")
    print("=" * 60)
    print(f"本地访问: http://localhost:{PORT}")
    print(f"手机访问: http://{ip}:{PORT}")
    print("=" * 60)
    print("可用页面:")
    print(f"  - 首页: http://localhost:{PORT}/index.html")
    print(f"  - MakerVerse: http://localhost:{PORT}/works.html")
    print(f"  - 学习资源: http://localhost:{PORT}/resources.html")
    print(f"  - 作品详情测试: http://localhost:{PORT}/test-work-detail.html")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)