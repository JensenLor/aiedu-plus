#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import socket
import os
import sys
import signal

httpd = None

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def signal_handler(signal_num, frame):
    global httpd
    if httpd:
        print("\n正在停止服务器...")
        httpd.shutdown()
        httpd.server_close()
        print("服务器已停止")
    sys.exit(0)

def main():
    global httpd
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Handler = http.server.SimpleHTTPRequestHandler
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if sys.platform == 'win32':
        try:
            import win32api
            import win32con
            
            def win32_handler(event):
                if event == win32con.CTRL_CLOSE_EVENT:
                    signal_handler(signal.SIGINT, None)
                    return 1
            
            win32api.SetConsoleCtrlHandler(win32_handler, True)
        except ImportError:
            pass
    
    for PORT in range(8000, 8100):
        try:
            httpd = socketserver.TCPServer(("", PORT), Handler)
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
            print("=" * 60)
            print("按 Ctrl+C 或关闭窗口停止服务器")
            print("=" * 60)
            
            httpd.serve_forever()
            return
        except OSError as e:
            if hasattr(e, 'winerror') and e.winerror == 10048:
                continue
            elif e.errno == 48:
                continue
            else:
                print(f"启动失败: {e}")
                input("按回车退出...")
                return
    
    print("错误: 所有端口都被占用")
    input("按回车退出...")

if __name__ == "__main__":
    main()