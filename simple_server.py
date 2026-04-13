#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单HTTP服务器 - 用于本地预览
"""

import os
import socket
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sys

def get_local_ip():
    """获取本地IP地址"""
    try:
        # 创建一个临时socket连接来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到Google DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """主函数"""
    # 设置工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 设置端口
    port = 8000
    
    # 获取IP地址
    ip_address = get_local_ip()
    
    print("=" * 50)
    print("🚀 罗辑智造社网站预览服务器")
    print("=" * 50)
    print()
    print(f"📂 网站目录: {os.getcwd()}")
    print(f"🌐 服务器地址: http://{ip_address}:{port}")
    print(f"💻 本地访问: http://localhost:{port}")
    print()
    print("📱 手机访问说明:")
    print("1. 确保手机和电脑在同一个WiFi网络")
    print("2. 在手机浏览器输入: http://" + ip_address + ":8000")
    print("3. 按Ctrl+C停止服务器")
    print("=" * 50)
    print()
    
    try:
        # 启动服务器
        server_address = ('', port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        
        # 尝试自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{port}')
        except:
            pass
        
        print(f"✅ 服务器已启动！正在监听端口 {port}")
        print("📂 可访问的文件:")
        print(f"   - 首页: http://localhost:{port}/index.html")
        print(f"   - 学生作品: http://localhost:{port}/cases.html")
        print(f"   - 个人主页示例: http://localhost:{port}/profile.html?id=zzy001")
        print()
        print("🔄 正在运行...")
        
        # 启动服务器
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n\n🛑 服务器已停止")
    except Exception as e:
        print(f"\n❌ 服务器启动失败: {e}")
        input("按Enter键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()